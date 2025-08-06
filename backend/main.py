"""
Main FastAPI application with restructured imports
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
import sys
import os
from pathlib import Path
from datetime import datetime
import logging

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import from restructured modules
from core.config import settings
from core.exceptions import (
    AccountNotFoundError, InsufficientFundsError, InvalidAmountError,
    account_not_found_handler, insufficient_funds_handler, 
    invalid_amount_handler, validation_exception_handler,
    general_exception_handler
)
from api import accounts

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Factory function to create FastAPI application"""
    
    # Create FastAPI app with production settings
    app = FastAPI(
        title=settings.app_name,
        description="A secure ATM system for account management",
        version="1.0.0",
        debug=settings.debug,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None
    )

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=settings.allowed_hosts
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"] if not settings.is_production else [],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Register exception handlers - order matters!
    app.add_exception_handler(AccountNotFoundError, account_not_found_handler)
    app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)
    app.add_exception_handler(InvalidAmountError, invalid_amount_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # Comment out general handler for now to allow specific handlers to work
    # app.add_exception_handler(Exception, general_exception_handler)

    # Include routers
    app.include_router(accounts.router)
    app.include_router(accounts.time_deposits_router)

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
            "debug": settings.debug,
            "version": "1.0.0"
        }

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port,
        reload=settings.debug
    )
