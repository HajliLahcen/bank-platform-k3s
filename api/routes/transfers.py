from flask import Blueprint, jsonify, request
from database.db import db

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from services.transfer_service import execute_transfer

from utils.metrics import (
    TRANSFER_SUCCESS,
    TRANSFER_FAILED
)


transfers_bp = Blueprint("transfers", __name__)


@transfers_bp.route("/transfer", methods=["POST"])
@jwt_required()
def transfer():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    claims = get_jwt()

    # Sender comes from JWT.
    # The browser cannot choose the sender.
    sender = claims.get("username")

    receiver = data.get("to")
    amount = data.get("amount")
    description = data.get("description")

    if not receiver:
        return jsonify({
            "error": "to is required"
        }), 400

    if amount is None:
        return jsonify({
            "error": "amount is required"
        }), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "error": "amount must be a number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "amount must be greater than zero"
        }), 400

    if receiver == sender:
        return jsonify({
            "error": "cannot transfer to your own account"
        }), 400

    try:

        transaction, error = execute_transfer(
            sender,
            receiver,
            amount,
            description
        )

        if error:
            TRANSFER_FAILED.inc()

            return jsonify({
                "error": error
            }), 400

        TRANSFER_SUCCESS.inc()

        return jsonify({
            "message": "transfer successful",
            "transaction": transaction.to_dict()
        }), 201

    except Exception as e:

        print(
            f"TRANSFER ERROR: {e}",
            flush=True
        )

        db.session.rollback()

        TRANSFER_FAILED.inc()

        return jsonify({
            "error": str(e)
        }), 500
