"""
Test configuration for FastAPI app
"""
from fastapi import FastAPI
from backend.main import create_app
from backend.database.test_db import db as test_db

def create_test_app() -> FastAPI:
    """Create FastAPI app configured for testing"""
    app = create_app()
    
    # Override database dependency to use the same test database instance
    from backend.api import accounts
    accounts.db = test_db
    
    return app

# Create test app instance
test_app = create_test_app()
