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
