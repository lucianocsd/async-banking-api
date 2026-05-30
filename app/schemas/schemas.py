from pydantic import BaseModel, ConfigDict, Field, AwareDatetime
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0, description="O valor deve ser maior que zero")

class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    created_at: AwareDatetime

    model_config = ConfigDict(from_attributes=True)

class AccountStatement(BaseModel):
    username: str
    balance: float
    transactions: List[TransactionResponse]

    model_config = ConfigDict(from_attributes=True)
