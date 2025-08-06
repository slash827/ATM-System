"""
Railway-compatible main application file
Simplified imports and error handling for deployment
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from fastapi.exceptions import RequestValidationError
    from datetime import datetime
    import logging
    
    # Try to import our modules
    from routers import accounts
    from exceptions import (
        AccountNotFoundError, InsufficientFundsError, InvalidAmountError,
        account_not_found_handler, insufficient_funds_handler, 
        invalid_amount_handler, validation_exception_handler,
        general_exception_handler
    )
    from config import settings
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Current working directory:", os.getcwd())
    print("Python path:", sys.path)
    print("Files in directory:", os.listdir('.'))
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app with production settings
app = FastAPI(
    title="ATM System API",
    description="A secure ATM system for account management",
    version="1.0.0",
    debug=False  # Always False for Railway
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # Allow all hosts for Railway
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for Railway
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
    return {"message": "ATM System is running on Railway!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "environment": "production"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting server on port {port}")
    
    uvicorn.run(
        "main_railway:app", 
        host="0.0.0.0", 
        port=port,
        reload=False
    )
