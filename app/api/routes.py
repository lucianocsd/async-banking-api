from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import timedelta
from app.db.database import get_db
from app.db.models import Account, Transaction
from app.schemas.schemas import UserCreate, Token, TransactionCreate, TransactionResponse, AccountStatement
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.api.dependencies import get_current_user

auth_router = APIRouter(prefix="/auth", tags=["auth"])
transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])
account_router = APIRouter(prefix="/account", tags=["account"])

@auth_router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(Account).where(Account.username == user.username)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username já registrado")
    
    hashed_password = get_password_hash(user.password)
    new_account = Account(username=user.username, hashed_password=hashed_password)
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": new_account.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(Account).where(Account.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@transactions_router.post("/deposit", response_model=TransactionResponse)
async def deposit(
    transaction: TransactionCreate, 
    current_user: Account = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor do depósito deve ser maior que zero")
    
    # Atualiza saldo e cria transação (tudo dentro de uma transaction do bd)
    current_user.balance += transaction.amount
    
    new_transaction = Transaction(
        account_id=current_user.id,
        type="deposit",
        amount=transaction.amount
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction


@transactions_router.post("/withdraw", response_model=TransactionResponse)
async def withdraw(
    transaction: TransactionCreate, 
    current_user: Account = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor do saque deve ser maior que zero")
    
    if current_user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    current_user.balance -= transaction.amount
    
    new_transaction = Transaction(
        account_id=current_user.id,
        type="withdrawal",
        amount=transaction.amount
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction


@account_router.get("/statement", response_model=AccountStatement)
async def get_statement(
    current_user: Account = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Account).options(selectinload(Account.transactions)).where(Account.id == current_user.id)
    result = await db.execute(query)
    user_with_transactions = result.scalars().first()
    
    return {
        "username": user_with_transactions.username,
        "balance": user_with_transactions.balance,
        "transactions": user_with_transactions.transactions
    }
