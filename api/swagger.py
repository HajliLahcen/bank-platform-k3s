from flask_restx import Namespace, Resource, fields


auth_ns = Namespace(
    "Authentication",
    description="Authentication operations"
)

accounts_ns = Namespace(
    "Accounts",
    description="Bank account operations"
)

transfers_ns = Namespace(
    "Transfers",
    description="Money transfer operations"
)

transactions_ns = Namespace(
    "Transactions",
    description="Transaction history"
)

metrics_ns = Namespace(
    "Monitoring",
    description="Monitoring and metrics"
)


# ============================
# Models
# ============================

login_model = auth_ns.model("Login", {
    "username": fields.String(
        required=True,
        example="lahcen"
    ),
    "password": fields.String(
        required=True,
        example="BankTest123!"
    )
})

register_model = auth_ns.model("Register", {
    "username": fields.String(
        required=True,
        example="newuser"
    ),
    "email": fields.String(
        required=True,
        example="user@bank.local"
    ),
    "password": fields.String(
        required=True,
        example="BankTest123!"
    )
})

account_model = accounts_ns.model("Account", {
    "username": fields.String(
        required=True,
        example="lahcen"
    ),
    "balance": fields.Float(
        required=True,
        example=1000
    )
})

transfer_model = transfers_ns.model("Transfer", {
    "from": fields.String(
        required=True,
        example="lahcen"
    ),
    "to": fields.String(
        required=True,
        example="rida"
    ),
    "amount": fields.Float(
        required=True,
        example=100
    ),
    "description": fields.String(
        example="Payment"
    )
})


# ============================
# Authentication
# ============================

@auth_ns.route("/register")
class Register(Resource):

    @auth_ns.expect(register_model)
    def post(self):
        """Register a new user"""
        return {
            "message": "Use POST /auth/register"
        }, 200


@auth_ns.route("/login")
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate and receive JWT"""
        return {
            "message": "Use POST /auth/login"
        }, 200


# ============================
# Accounts
# ============================

@accounts_ns.route("/accounts")
class Accounts(Resource):

    def get(self):
        """Get all bank accounts"""
        return {
            "message": "Use GET /accounts"
        }, 200

    @accounts_ns.expect(account_model)
    def post(self):
        """Create a bank account"""
        return {
            "message": "Use POST /accounts"
        }, 201


@accounts_ns.route("/balance/<string:username>")
class Balance(Resource):

    def get(self, username):
        """Get account balance"""
        return {
            "message": f"Use GET /balance/{username}"
        }, 200


# ============================
# Transfers
# ============================

@transfers_ns.route("/transfer")
class Transfer(Resource):

    @transfers_ns.expect(transfer_model)
    def post(self):
        """Execute a bank transfer"""
        return {
            "message": "Use POST /transfer"
        }, 201


# ============================
# Transactions
# ============================

@transactions_ns.route("/transactions")
class Transactions(Resource):

    def get(self):
        """Get all transactions"""
        return {
            "message": "Use GET /transactions"
        }, 200


@transactions_ns.route("/transactions/<string:username>")
class UserTransactions(Resource):

    def get(self, username):
        """Get transactions for a user"""
        return {
            "message": f"Use GET /transactions/{username}"
        }, 200


# ============================
# Metrics
# ============================

@metrics_ns.route("/metrics")
class Metrics(Resource):

    def get(self):
        """Get Prometheus metrics"""
        return {
            "message": "Prometheus metrics available at /metrics"
        }, 200
