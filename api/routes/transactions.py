from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.transaction_service import (
    get_all_transactions,
    get_account_transactions
)


transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():

    claims = get_jwt()
    current_username = claims.get("username")
    current_role = claims.get("role")

    if current_role == "ADMIN":
        transactions = get_all_transactions()
    else:
        transactions = get_account_transactions(
            current_username
        )

    return jsonify([
        transaction.to_dict()
        for transaction in transactions
    ])


@transactions_bp.route(
    "/transactions/<string:username>",
    methods=["GET"]
)
@jwt_required()
def get_user_transactions(username):

    claims = get_jwt()
    current_username = claims.get("username")
    current_role = claims.get("role")

    if current_role != "ADMIN" and username != current_username:
        return jsonify({
            "error": "you can only access your own transactions"
        }), 403

    transactions = get_account_transactions(username)

    return jsonify([
        transaction.to_dict()
        for transaction in transactions
    ])
