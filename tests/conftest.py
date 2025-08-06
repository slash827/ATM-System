"""
Test configuration and utilities
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from backend.main import create_app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    app = create_app()
    return TestClient(app)

@pytest.fixture
def test_account():
    """Provide a test account number"""
    return "123456"

@pytest.fixture
def invalid_account():
    """Provide an invalid account number"""
    return "999999"
