from flask import Blueprint, jsonify
from models.account import Account

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
def get_accounts():

    accounts = Account.query.all()

    return jsonify(
        [account.to_dict() for account in accounts]
    )
