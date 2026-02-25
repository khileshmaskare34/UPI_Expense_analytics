from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

from app.core.deps import get_current_user, get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.crud.transaction import create_transaction
from app.models.user import User
from app.models.transaction import Transaction

from app.crud.transaction import create_transaction, get_all_transactions
from typing import List


from fastapi import HTTPException
from app.crud.transaction import update_transaction
from app.services.ml_service import predict_category

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse)
def add_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If category not provided → use ML
    if data.category_id is None:
        predicted_category = predict_category(data.description)
        data.category_id = predicted_category

    txn = create_transaction(db, current_user.id, data)
    return txn


@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    print("yes its working")
    txns = get_all_transactions(db, current_user.id)
    return txns


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction_api(
    transaction_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    trx = update_transaction(db, transaction_id, data)

    if not trx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Make sure user can update ONLY his transaction
    if trx.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return trx

@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Only allow user to delete their own transaction
    if transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this transaction")

    db.delete(transaction)
    db.commit()
    return