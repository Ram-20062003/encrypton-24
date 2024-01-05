from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(unique=True)
    name: str
    password: str
    mobile_no: int

class UserLogin(SQLModel):
    email: str
    password: str



    


