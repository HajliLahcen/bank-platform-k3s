from database.db import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    reference = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    from_account = db.Column(
        db.String(50),
        nullable=False
    )

    to_account = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "reference": self.reference,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "amount": float(self.amount),
            "status": self.status,
            "description": self.description,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }
