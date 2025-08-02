from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from routers import accounts
from exceptions import (
    AccountNotFoundError, InsufficientFundsError, InvalidAmountError,
    account_not_found_handler, insufficient_funds_handler, 
    invalid_amount_handler, validation_exception_handler,
    general_exception_handler
)
from config import settings
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app with production settings
app = FastAPI(
    title=settings.app_name,
    description="A secure ATM system for account management",
    version="1.0.0",
    debug=settings.debug,  # Only True in development
    docs_url="/docs" if not settings.is_production else None,  # Hide docs in production
    redoc_url="/redoc" if not settings.is_production else None
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.allowed_hosts
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(AccountNotFoundError, account_not_found_handler)
app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)
app.add_exception_handler(InvalidAmountError, invalid_amount_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(accounts.router)

# Basic endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "ATM System is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "environment": settings.environment,
        "debug": settings.debug
    }