from werkzeug.security import generate_password_hash, check_password_hash

from database.db import db
from models.user import User


def register_user(username, email, password):

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return None, "username already exists"

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return None, "email already exists"

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role="USER"
    )

    db.session.add(user)
    db.session.commit()

    return user, None


def authenticate_user(username, password):

    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return None

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return None

    return user
