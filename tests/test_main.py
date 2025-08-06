from fastapi.testclient import TestClient
from backend.main import app

# DON'T create client at module level - create inside functions!

def test_root_endpoint():
    """Test root endpoint returns correct message"""
    with TestClient(app, raise_server_exceptions=False) as client:  # Use context manager
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "ATM System is running!"}

def test_health_check():
    """Test health check endpoint"""
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

def test_docs_accessible():
    """Test that API documentation is accessible"""
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/docs")
        assert response.status_code == 200

def test_openapi_schema():
    """Test that OpenAPI schema is available"""
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "ATM System API"