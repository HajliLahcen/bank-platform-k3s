from flask import Blueprint, jsonify, request
from database.db import db
from services.transfer_service import execute_transfer
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import get_jwt
from utils.metrics import (
    TRANSFER_SUCCESS,
    TRANSFER_FAILED
)

transfers_bp = Blueprint("transfers", __name__)


@transfers_bp.route("/transfer", methods=["POST"])
@jwt_required()

def transfer():

    data = request.get_json()
    claims = get_jwt()
    current_username = claims.get("username")
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    sender = data.get("from")
    if sender != current_username:
        return jsonify({
           "error": "you can only transfer from your own account"
        }), 403
    receiver = data.get("to")
    amount = data.get("amount")
    description = data.get("description")

    if not sender:
        return jsonify({
            "error": "from is required"
        }), 400

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

    try:
        transaction, error = execute_transfer(
            sender,
            receiver,
            amount,
            description
        )

        if error:
            return jsonify({
                "error": error
            }), 400

        return jsonify({
            "message": "transfer successful",
            "transaction": transaction.to_dict()
        }), 201

    
    except Exception as e:
        print(f"TRANSFER ERROR: {e}", flush=True)
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500
