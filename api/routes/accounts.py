from flask import Blueprint, jsonify, request
import time

from flask_jwt_extended import jwt_required, get_jwt

from utils.metrics import REQUEST_COUNT, REQUEST_LATENCY
from services.account_service import (
    get_all_accounts,
    get_account,
    create_account
)

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
@jwt_required()
def get_accounts():

    start = time.time()

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/accounts"
    ).inc()

    claims = get_jwt()
    current_username = claims.get("username")

    account = get_account(current_username)

    REQUEST_LATENCY.observe(
        time.time() - start
    )

    if not account:
        return jsonify({
            "error": "account not found"
        }), 404

    return jsonify(
        account.to_dict()
    )


@accounts_bp.route("/beneficiaries", methods=["GET"])
@jwt_required()
def get_beneficiaries():

    claims = get_jwt()
    current_username = claims.get("username")

    accounts = get_all_accounts()

    beneficiaries = [
        {
            "username": account.username
        }
        for account in accounts
        if account.username != current_username
    ]

    return jsonify(beneficiaries)


@accounts_bp.route("/accounts", methods=["POST"])
@jwt_required()
def create_account_route():

    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({
            "error": "admin access required"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    balance = data.get("balance")

    if not username:
        return jsonify({
            "error": "username is required"
        }), 400

    if balance is None:
        return jsonify({
            "error": "balance is required"
        }), 400

    try:
        balance = float(balance)
    except (TypeError, ValueError):
        return jsonify({
            "error": "balance must be a number"
        }), 400

    if balance < 0:
        return jsonify({
            "error": "balance cannot be negative"
        }), 400

    account, error = create_account(
        username,
        balance
    )

    if error:
        return jsonify({
            "error": error
        }), 409

    return jsonify(
        account.to_dict()
    ), 201


@accounts_bp.route(
    "/balance/<string:username>",
    methods=["GET"]
)
@jwt_required()
def get_balance(username):

    claims = get_jwt()
    current_username = claims.get("username")

    if (
        claims.get("role") != "ADMIN"
        and username != current_username
    ):
        return jsonify({
            "error": "you can only access your own balance"
        }), 403

    account = get_account(username)

    if not account:
        return jsonify({
            "error": "user not found"
        }), 404

    return jsonify({
        "username": account.username,
        "balance": float(account.balance)
    })
