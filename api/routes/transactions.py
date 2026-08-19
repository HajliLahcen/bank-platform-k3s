from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from services.transaction_service import (
    get_all_transactions,
    get_account_transactions
)


transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():

    transactions = get_all_transactions()

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

    transactions = get_account_transactions(username)

    return jsonify([
        transaction.to_dict()
        for transaction in transactions
    ])
