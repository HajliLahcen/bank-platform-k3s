import uuid
from decimal import Decimal, InvalidOperation
from models.transaction import Transaction
from database.db import db
from models.account import Account
from models.transaction import Transaction


def get_all_transactions():
    return (
        Transaction.query
        .order_by(Transaction.created_at.desc())
        .all()
    )


def get_account_transactions(username):
    return (
        Transaction.query
        .filter(
            (Transaction.from_account == username)
            | (Transaction.to_account == username)
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )



def execute_transfer(
    sender_username,
    receiver_username,
    amount,
    description=None
):
    if sender_username == receiver_username:
        return None, "sender and receiver cannot be the same"

    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError):
        return None, "amount must be a valid number"

    if amount <= Decimal("0"):
        return None, "amount must be greater than zero"

    sender = Account.query.filter_by(
        username=sender_username
    ).first()

    if not sender:
        return None, "sender not found"

    receiver = Account.query.filter_by(
        username=receiver_username
    ).first()

    if not receiver:
        return None, "receiver not found"

    if sender.balance < amount:
        return None, "insufficient funds"

    try:
        sender.balance -= amount
        receiver.balance += amount

        transaction = Transaction(
            reference=str(uuid.uuid4()),
            from_account=sender.username,
            to_account=receiver.username,
            amount=amount,
            status="SUCCESS",
            description=description
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction, None

    except Exception:
        db.session.rollback()
        raise
