from flask import Blueprint, jsonify, request

from services.account_service import (
    get_all_accounts,
    get_account,
    create_account
)


accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
def get_accounts():

    accounts = get_all_accounts()

    return jsonify(
        [account.to_dict() for account in accounts]
    )


@accounts_bp.route("/accounts", methods=["POST"])
def create_account_route():

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
def get_balance(username):

    account = get_account(username)

    if not account:
        return jsonify({
            "error": "user not found"
        }), 404

    return jsonify({
        "username": account.username,
        "balance": float(account.balance)
    })
