from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from services.auth_service import (
    register_user,
    authenticate_user
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username:
        return jsonify({
            "error": "username is required"
        }), 400

    if not email:
        return jsonify({
            "error": "email is required"
        }), 400

    if not password:
        return jsonify({
            "error": "password is required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "password must contain at least 8 characters"
        }), 400

    user, error = register_user(
        username,
        email,
        password
    )

    if error:
        return jsonify({
            "error": error
        }), 409

    return jsonify({
        "message": "user created",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }), 400

    user = authenticate_user(
        username,
        password
    )

    if not user:
        return jsonify({
            "error": "invalid credentials"
        }), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role
        }
    )

    return jsonify({
        "access_token": token,
        "user": user.to_dict()
    })
