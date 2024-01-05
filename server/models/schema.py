
from typing import Optional
from sqlalchemy import table
from sqlmodel import Field
from server.models.transaction import TransactionBase

from server.models.user import UserBase

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    client_ip: str = Field(default="")