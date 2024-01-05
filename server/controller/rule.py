from server.models.schema import Transaction
from server.models.transaction import TransactionBase
from sqlmodel import Session, select
from fastapi.param_functions import Depends

def is_fraud(transaction: TransactionBase,   database: Session):
    print(transaction.sender_name)
    user_amount = database.exec(select(Transaction).where(Transaction.sender_name == transaction.sender_name).order_by(Transaction.amount)).all()    
    user_lower_amount= user_amount[0].amount
    user_higher_amount= user_amount[-1].amount
    
    if user_lower_amount and user_higher_amount:
        if transaction.amount > user_higher_amount.amount*5:
            return 1
    user_time = database.exec(select(Transaction).where(Transaction.sender_name == transaction.sender_name and Transaction.time == transaction.time)).all()
    
    if len(user_time) > 3:
        return 1
    
    if transaction.amount > 2000000:
            return 1
    if transaction.sender_old_balance - transaction.sender_new_balance - transaction.amount < 0:
            return 1
    
    return 0
