from http.server import HTTPServer, BaseHTTPRequestHandler
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import psycopg2
import json
import os
import time


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# ============================
# Prometheus Metrics
# ============================

REQUEST_COUNT = Counter(
    "bank_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

TRANSFER_SUCCESS = Counter(
    "bank_transfer_success_total",
    "Successful bank transfers"
)

TRANSFER_FAILED = Counter(
    "bank_transfer_failed_total",
    "Failed bank transfers"
)

REQUEST_LATENCY = Histogram(
    "bank_request_duration_seconds",
    "HTTP request latency"
)


class BankAPI(BaseHTTPRequestHandler):

    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors_headers()
        self.end_headers()

    def do_GET(self):

        # ============================
        # /metrics
        # ============================
        if self.path == "/metrics":

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()

            self.wfile.write(generate_latest())
            return

        # ============================
        # /accounts
        # ============================

        elif self.path == "/accounts":

            REQUEST_COUNT.labels(
                method="GET",
                endpoint="/accounts"
            ).inc()

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT username, balance FROM accounts"
            )

            rows = cur.fetchall()

            cur.close()
            conn.close()

            accounts = []

            for row in rows:
                accounts.append({
                    "username": row[0],
                    "balance": float(row[1])
                })

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(accounts).encode()
            )

        # ============================
        # /balance
        # ============================

        elif self.path.startswith("/balance/"):

            REQUEST_COUNT.labels(
                method="GET",
                endpoint="/balance"
            ).inc()

            username = self.path.split("/")[-1]

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
                (username,)
            )

            result = cur.fetchone()

            cur.close()
            conn.close()

            if result:

                response = {
                    "username": username,
                    "balance": float(result[0])
                }

                self.send_response(200)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps(response).encode()
                )

            else:

                self.send_response(404)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    b'{"error":"user not found"}'
                )

        else:

            self.send_response(404)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"error":"endpoint not found"}'
            )


    def do_POST(self):

        if self.path == "/transfer":

            REQUEST_COUNT.labels(
                method="POST",
                endpoint="/transfer"
            ).inc()

            start = time.time()

            content_length = int(
                self.headers["Content-Length"]
            )

            body = self.rfile.read(content_length)

            data = json.loads(body.decode())

            sender = data["from"]
            receiver = data["to"]
            amount = float(data["amount"])

            conn = get_connection()
            cur = conn.cursor()

            # -----------------------------
            # Check sender
            # -----------------------------

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
                (sender,)
            )

            result = cur.fetchone()

            if not result:

                TRANSFER_FAILED.inc()

                REQUEST_LATENCY.observe(
                    time.time() - start
                )

                self.send_response(404)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    b'{"error":"sender not found"}'
                )

                cur.close()
                conn.close()
                return

            sender_balance = float(result[0])

            # -----------------------------
            # Check receiver
            # -----------------------------

            cur.execute(
                "SELECT balance FROM accounts WHERE username=%s",
                (receiver,)
            )

            receiver_result = cur.fetchone()

            if not receiver_result:

                TRANSFER_FAILED.inc()

                REQUEST_LATENCY.observe(
                    time.time() - start
                )

                self.send_response(404)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    b'{"error":"receiver not found"}'
                )

                cur.close()
                conn.close()
                return

            # -----------------------------
            # Check balance
            # -----------------------------

            if sender_balance < amount:

                TRANSFER_FAILED.inc()

                REQUEST_LATENCY.observe(
                    time.time() - start
                )

                self.send_response(400)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    b'{"error":"insufficient funds"}'
                )

                cur.close()
                conn.close()
                return

            # -----------------------------
            # Debit sender
            # -----------------------------

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE username = %s
                """,
                (amount, sender)
            )

            # -----------------------------
            # Credit receiver
            # -----------------------------

            cur.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE username = %s
                """,
                (amount, receiver)
            )

            conn.commit()

            TRANSFER_SUCCESS.inc()

            REQUEST_LATENCY.observe(
                time.time() - start
            )

            cur.close()
            conn.close()

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"status":"transfer successful"}'
            )

        else:

            self.send_response(404)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"error":"endpoint not found"}'
            )

 
server = HTTPServer(
    ("0.0.0.0", 8000),
    BankAPI
)

print("Bank API started on port 8000")

server.serve_forever()
