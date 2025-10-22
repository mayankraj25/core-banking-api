from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . core.config import settings
from . api.v1 import auth, accounts, transactions

app=FastAPI(title=settings.PROJECT_NAME,
            version="1.0.0",
            description="Digital Banking managemenet system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(accounts.router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Banking System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}