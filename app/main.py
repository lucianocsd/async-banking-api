from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.api.routes import auth_router, transactions_router, account_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa as tabelas no banco de dados SQLite (apenas para ambiente de dev/desafio)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="API Bancária Assíncrona",
    description="Desafio de API RESTful assíncrona usando FastAPI para gerenciar operações bancárias.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(account_router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Bancária Assíncrona. Acesse /docs para a documentação."}
