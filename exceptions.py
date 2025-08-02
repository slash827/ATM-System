from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import sys
import os

# Add current directory to Python path for Railway deployment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import settings
except ImportError:
    # Fallback for deployment environments
    class FallbackSettings:
        debug = False
        environment = "production"
        log_level = "INFO"
    settings = FallbackSettings()

logger = logging.getLogger(__name__)

# Custom exceptions (same as before)
class AccountNotFoundError(Exception):
    """Raised when account is not found"""
    def __init__(self, account_number: str):
        self.account_number = account_number
        super().__init__(f"Account {account_number} not found")

class InsufficientFundsError(Exception):
    """Raised when withdrawal amount exceeds balance"""
    def __init__(self, account_number: str, balance: float, amount: float):
        self.account_number = account_number
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds. Balance: {balance}, Requested: {amount}")

class InvalidAmountError(Exception):
    """Raised when amount is invalid"""
    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid amount: {amount}")

# Enhanced exception handlers with security logging
async def account_not_found_handler(request: Request, exc: AccountNotFoundError):
    """Handle account not found errors"""
    client_ip = request.client.host
    logger.warning(f"Account not found attempt from {client_ip}: {exc.account_number}")
    
    return JSONResponse(
        status_code=404,
        content={
            "error": "Account Not Found",
            "detail": "The specified account does not exist" if settings.is_production 
                     else str(exc),
            "account_number": exc.account_number if not settings.is_production else None
        }
    )

async def insufficient_funds_handler(request: Request, exc: InsufficientFundsError):
    """Handle insufficient funds errors"""
    client_ip = request.client.host
    logger.info(f"Insufficient funds attempt from {client_ip}: {exc.account_number}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Insufficient Funds",
            "detail": "Transaction amount exceeds available balance" if settings.is_production 
                     else str(exc),
            "current_balance": float(exc.balance) if not settings.is_production and exc.balance is not None else None,
            "requested_amount": float(exc.amount) if not settings.is_production and exc.amount is not None else None
        }
    )

async def invalid_amount_handler(request: Request, exc: InvalidAmountError):
    """Handle invalid amount errors"""
    client_ip = request.client.host
    logger.warning(f"Invalid amount attempt from {client_ip}: {exc.amount}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid Amount",
            "detail": "The amount provided is invalid" if settings.is_production 
                     else str(exc),
            "amount": float(exc.amount) if not settings.is_production and exc.amount is not None else None
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    client_ip = request.client.host
    logger.warning(f"Validation error from {client_ip}: {exc.errors()}")
    
    # Clean up errors to make them JSON serializable
    clean_errors = []
    if not settings.is_production:
        for error in exc.errors():
            clean_error = {
                "type": error.get("type"),
                "loc": error.get("loc"),
                "msg": error.get("msg"),
                "input": error.get("input")
            }
            clean_errors.append(clean_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Invalid input data",
            "errors": clean_errors
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    client_ip = request.client.host
    logger.error(f"Unexpected error from {client_ip}: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred" if settings.is_production 
                     else str(exc)
        }
    )