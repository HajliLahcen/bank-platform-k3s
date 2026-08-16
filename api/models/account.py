from database.db import db


class Account(db.Model):
    __tablename__ = "accounts"

    username = db.Column(
        db.String(50),
        primary_key=True,
        nullable=False
    )

    balance = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    def to_dict(self):
        return {
            "username": self.username,
            "balance": float(self.balance)
        }
