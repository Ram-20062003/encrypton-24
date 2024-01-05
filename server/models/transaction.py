from decimal import Decimal
from sqlmodel import SQLModel, Field

class TransactionBase(SQLModel):
    time: int
    amount: Decimal
    sender_name: str
    sender_old_balance: Decimal
    sender_new_balance: Decimal
    receiver_name: str
    receiver_old_balance: Decimal
    receiver_new_balance: Decimal
    transaction_type: str
    is_fraud: int = -1