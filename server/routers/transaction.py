from fastapi import APIRouter, HTTPException, Request
from fastapi.param_functions import Depends
from sqlmodel import Session, select
from server.controller.auth import get_current_user, get_password_hash, verify_password
from server.controller.transaction import predict
from server.models.schema import *
from config.database import get_database
from server.models.transaction import TransactionBase
from server.controller.auth import sign_jwt, JWTBearer


router = APIRouter(
    prefix="/transaction",
)

@router.post("/create")
async def start_transaction(
    transaction: TransactionBase,
    request: Request,
    bearer_token: str = Depends(JWTBearer()),
    database: Session = Depends(get_database),
):
    user = get_current_user(bearer_token, database)
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid User")
    if not request.client:
        raise HTTPException(status_code=401, detail="Invalid Client")
    trans  = Transaction(
        user_id=user.id,
        amount=transaction.amount,
        sender_name=transaction.sender_name,
        receiver_name=transaction.receiver_name,
        receiver_new_balance=transaction.receiver_new_balance,
        receiver_old_balance=transaction.receiver_old_balance,
        sender_new_balance=transaction.sender_new_balance,
        sender_old_balance=transaction.sender_old_balance,
        time=transaction.time,
        client_ip=request.client.host,
        transaction_type=transaction.transaction_type,
    )
    database.add(trans)
    database.commit()
    database.refresh(trans)

    print(database)
    
    await predict(trans,database)
    database.close()
    return {"message": "Transaction Created"}


@router.post("/csv")
async def start_transactions(
    transactions: list[TransactionBase],
    request: Request,
    bearer_token: str = Depends(JWTBearer()),
    database: Session = Depends(get_database),
):
    user = get_current_user(bearer_token, database)
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid User")
    if not request.client:
        raise HTTPException(status_code=401, detail="Invalid Client")
    for transaction in transactions:

        trans  = Transaction(
            user_id=user.id,
            amount=transaction.amount,
            sender_name=transaction.sender_name,
            receiver_name=transaction.receiver_name,
            receiver_new_balance=transaction.receiver_new_balance,
            receiver_old_balance=transaction.receiver_old_balance,
            sender_new_balance=transaction.sender_new_balance,
            sender_old_balance=transaction.sender_old_balance,
            time=transaction.time,
            client_ip=request.client.host,
            transaction_type=transaction.transaction_type,
        )
        database.add(trans)
        database.commit()
        database.refresh(trans)

        print(database)
        
        await predict(trans,database)
    database.close()
    return {"message": "Transaction Created"}

@router.get("/get/{page}")
async def get_transactions(
    page: int,
    bearer_token: str = Depends(JWTBearer()),
    database: Session = Depends(get_database),
):
    user = get_current_user(bearer_token, database)
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    # count total transactions
    count = len(database.exec(select(Transaction).where(Transaction.user_id == user.id)).all())
    
    # recent transactions 10
    transactions = database.exec(select(Transaction).where(Transaction.user_id == user.id).limit(10+1).offset(page * 10)).all()
    database.close()
    return {
        "count": count,
        "transactions": transactions
    }