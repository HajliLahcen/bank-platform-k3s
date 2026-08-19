from flask import Flask, jsonify
from flask_migrate import Migrate
from routes.transfers import transfers_bp
from config import Config
from database.db import db
from routes.health import health_bp
from routes.accounts import accounts_bp
from routes.transactions import transactions_bp
from routes.metrics import metrics_bp
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from flask_restx import Api
from swagger import (
    auth_ns,
    accounts_ns,
    transfers_ns,
    transactions_ns,
    metrics_ns
)


app = Flask(__name__)

api = Api(
    app,
    title="Bank Platform API",
    version="2.0",
    description="Banking REST API",
    doc="/swagger/"
)

api.add_namespace(
    auth_ns,
    path="/auth"
)

api.add_namespace(
    accounts_ns
)

api.add_namespace(
    transfers_ns
)

api.add_namespace(
    transactions_ns
)

api.add_namespace(
    metrics_ns
)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(health_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(transfers_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return jsonify({
        "application": "Bank Platform",
        "version": "2.0",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )
