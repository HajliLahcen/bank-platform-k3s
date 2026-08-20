import os

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db

# Import models so SQLAlchemy / Flask-Migrate knows about them
from models.account import Account
from models.transaction import Transaction
from models.user import User

# Routes
from routes.health import health_bp
from routes.accounts import accounts_bp
from routes.transfers import transfers_bp
from routes.transactions import transactions_bp
from routes.metrics import metrics_bp
from routes.auth import auth_bp


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

app.config.from_object(Config)


# ==========================================
# Database
# ==========================================

db.init_app(app)

migrate = Migrate(
    app,
    db
)


# ==========================================
# JWT Authentication
# ==========================================

jwt = JWTManager(app)


# ==========================================
# Routes / Blueprints
# ==========================================

app.register_blueprint(
    health_bp
)

app.register_blueprint(
    accounts_bp
)

app.register_blueprint(
    transfers_bp
)

app.register_blueprint(
    transactions_bp
)

app.register_blueprint(
    metrics_bp
)

app.register_blueprint(
    auth_bp
)


# ==========================================
# Basic Error Handlers
# ==========================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "error": "internal server error"
    }), 500


# ==========================================
# Application Start
# ==========================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    print(
        f"Bank API started on port {port}"
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
