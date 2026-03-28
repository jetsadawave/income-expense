from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    date: date

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    date: date
    user_id: int

    class Config:
        from_attributes = True
