from flask import Flask, jsonify

from config import Config
from database.db import db
from routes.health import health_bp
from routes.accounts import accounts_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(health_bp)
app.register_blueprint(accounts_bp)


@app.route("/")
def home():
    return jsonify({
        "application": "Bank Platform",
        "version": "2.0",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
