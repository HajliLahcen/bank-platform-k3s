from database.db import db
from models.account import Account


def get_all_accounts():
    return Account.query.all()


def get_account(username):
    return Account.query.filter_by(
        username=username
    ).first()


def create_account(username, balance):

    existing_account = get_account(username)

    if existing_account:
        return None, "account already exists"

    account = Account(
        username=username,
        balance=balance
    )

    db.session.add(account)
    db.session.commit()

    return account, None
