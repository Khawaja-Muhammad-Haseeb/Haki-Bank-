"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, users, accounts, transactions, bills, admin

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="HakiBank Online Banking System API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(bills.router)
app.include_router(admin.router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
