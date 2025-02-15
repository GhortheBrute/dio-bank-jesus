from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

tags_metadata = [
    {
        "name": "auth",
        "description": "API de autenticação",
    },
    {
        "name": "account",
        "description": "API de gerenciamento de contas",
    },
    {
        "name": "transaction",
        "description": "API de transacao de contas",
    },
]

app = FastAPI(
    title="DIO BANK - Jesus",
    version="1.0.0",
    summary="Serviço de gerenciamento de transações de depósito e retirada."
    description="""
    DIO BANK - Jesus é um serviço de gerenciamento de transações bancárias.
    
    ## Account
    
    * **Criar contas**,
    * **Listar contas**,
    * **Listar transações da conta por ID**,
    
    ## Transaction
    
    * **Criar transacao**,
    """,
        openapi_tags=tags_metadata,
        redoc_url=None,
        lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(account.router, tags=["conta"])
app.include_router(transaction.router, tags=["transação"])

@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc): AccountNotFoundError = AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found"})

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})