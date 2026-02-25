from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.schemas.transaction import TransactionUpdate


def create_transaction(db: Session, user_id: int, data: TransactionCreate):
    new_txn = Transaction(
        amount=data.amount,
        description=data.description,
        category_id=data.category_id,
        user_id=user_id
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

def get_all_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()

def update_transaction(db: Session, transaction_id: int, data: TransactionUpdate):
    trx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not trx:
        return None

    if data.amount is not None:
        trx.amount = data.amount

    if data.description is not None:
        trx.description = data.description

    if data.category_id is not None:
        trx.category_id = data.category_id

    db.commit()
    db.refresh(trx)
    return trx