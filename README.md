# Bank System Website

A robust, secure Bank system built with FastAPI, featuring comprehensive financial operations, advanced security measures, and production-ready Docker deployment.

![Tests](https://img.shields.io/badge/tests-43%2F43%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)
![Pydantic](https://img.shields.io/badge/Pydantic-2.11.5-orange)
![Security](https://img.shields.io/badge/Docker-Hardened-blue)

## 🏧 Features

### Core Banking Operations
- **Account Balance Inquiry** - Check current account balance with precise decimal handling
- **Money Withdrawal** - Secure withdrawals with balance validation and transaction logging
- **Money Deposit** - Fund deposits with amount validation and audit trails
- **Transaction History** - Timestamp tracking for all operations

### Security & Validation
- **Financial Precision** - Decimal-based arithmetic to avoid floating-point errors
- **Input Validation** - Comprehensive request validation with Pydantic v2
- **Security Hardening** - XSS prevention, input sanitization, and malicious input protection
- **Path Validation** - Account number format enforcement (6-digit pattern)
- **Error Handling** - Secure error responses without information leakage

### Development & Deployment
- **API Documentation** - Auto-generated interactive docs with OpenAPI 3.0
- **Comprehensive Testing** - 43 tests covering all scenarios and edge cases
- **Docker Security** - Hardened multi-stage builds with distroless runtime
- **Production Ready** - Environment-based configuration and monitoring

## 🛠️ **Major Updates & Improvements**

### **1. Pydantic v2 Migration & Financial Precision**

**Challenge**: The system was using deprecated Pydantic v1 syntax and floating-point arithmetic for financial calculations, leading to precision issues.

**Solutions Implemented**:
- **Pydantic v2 Upgrade**: Migrated from `regex` → `pattern`, `validator` → `field_validator`
- **Decimal Precision**: Replaced all `float` types with `Decimal` for financial accuracy
- **JSON Serialization**: Custom `model_serializer` for proper Decimal → float conversion in API responses
- **Type Safety**: Ensured consistent Decimal usage throughout the application

**Before vs After**:
```python
# Before (Pydantic v1 + Float)
class Account(BaseModel):
    balance: float = Field(ge=0, regex=r"^\d{6}$")
    
    @validator('balance')
    def validate_balance(cls, v):
        return round(v, 2)

# After (Pydantic v2 + Decimal)
class Account(BaseModel):
    balance: Decimal = Field(ge=0, pattern=r"^\d{6}$")
    
    @field_validator('balance')
    @classmethod
    def validate_balance(cls, v):
        return Decimal(str(v)).quantize(Decimal('0.01'))
```

### **2. Comprehensive Test Suite Expansion**

**Achievement**: Expanded from 18 to **43 comprehensive tests** (139% increase)

**Test Categories**:
- **Account Operations** (14 tests): Balance queries, deposits, withdrawals, transaction sequences
- **Decimal Precision** (13 tests): Financial arithmetic, rounding consistency, floating-point prevention
- **Security Validation** (12 tests): Input sanitization, XSS prevention, malicious input handling
- **Main Endpoints** (4 tests): Health checks, API documentation, OpenAPI schema

**Advanced Test Scenarios**:
```python
# Financial Security Tests
def test_salami_slicing_prevention():
    """Prevent micro-fraction manipulation attacks"""
    
def test_floating_point_precision_issues():
    """Ensure Decimal prevents 0.1 + 0.2 != 0.3 issues"""

# Security Tests  
def test_xss_prevention():
    """Test XSS attack prevention in account numbers"""
    
def test_null_byte_injection():
    """Test null byte injection attempts"""
```

### **3. Docker Security Hardening**

**Challenge**: Original Docker image had 3-4 high security vulnerabilities.

**Security Improvements**:
- **Multi-stage Builds**: Separates build dependencies from runtime
- **Distroless Runtime**: Google's distroless Python image (minimal attack surface)
- **Version Matching**: Exact Python 3.11.2 version to match development environment
- **Security Scanning**: Integrated `pip audit` for dependency vulnerability detection
- **Non-root Execution**: Runs as non-privileged user by default

**Vulnerability Reduction**:
```dockerfile
# Before: Alpine with 3-4 high vulnerabilities
FROM python:3.11-alpine

# After: Distroless with 2 high vulnerabilities (50% reduction)
FROM gcr.io/distroless/python3-debian12:nonroot
```

### **4. Enhanced Error Handling & JSON Serialization**

**Challenge**: Exception handlers were failing to serialize Decimal values in JSON responses.

**Solutions**:
- **Clean Serialization**: Convert Decimal to float in exception handlers
- **Validation Routing**: Added path parameter validation for proper 422 vs 404 error handling
- **Security Logging**: Environment-aware error details (verbose in dev, generic in production)

**Example Fix**:
```python
# Before: JSON serialization error
"current_balance": exc.balance  # Decimal object fails

# After: Proper serialization  
"current_balance": float(exc.balance) if exc.balance else None
```

## 📁 **Project Structure**
```
atm-system/
├── main.py                     # FastAPI application entry point
├── models.py                   # Pydantic v2 models with Decimal precision
├── database.py                 # In-memory storage with Decimal handling
├── security.py                 # Security middleware (CORS, rate limiting)
├── config.py                   # Environment-based configuration
├── exceptions.py               # Custom exceptions with JSON serialization
├── routers/
│   ├── __init__.py
│   └── accounts.py             # ATM endpoints with path validation
├── tests/                      # Comprehensive test suite (43 tests)
│   ├── __init__.py
│   ├── test_main.py            # Basic app tests (4 tests)
│   ├── test_accounts.py        # ATM endpoint tests (14 tests)
│   ├── test_decimal_precision.py # Financial precision tests (13 tests)
│   └── test_security.py        # Security validation tests (12 tests)
├── pytest.ini                 # Test configuration
├── requirements.txt            # Pinned dependencies (production-ready)
├── Dockerfile                  # Hardened multi-stage Docker build
├── Dockerfile.secure           # Ultra-secure Chainguard alternative
├── docker-compose.secure.yml   # Production deployment configuration
├── .dockerignore              # Docker build optimization
├── DOCKER_SECURITY.md         # Docker security documentation
├── verify_compatibility.py    # Environment verification script
└── README.md                  # Comprehensive documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11.2 (exact version for Docker compatibility)
- pip package manager
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd atm-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux  
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify environment compatibility**
```bash
python verify_compatibility.py
```

5. **Run the server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Test Accounts
The system comes with pre-configured test accounts:

| Account Number | Initial Balance |
|---------------|----------------|
| 123456        | $1,000.00      |
| 789012        | $500.00        |
| 555444        | $0.00          |

### Endpoints

#### 1. Get Account Balance
```http
GET /accounts/{account_number}/balance
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/accounts/123456/balance"
```

**Example Response:**
```json
{
  "account_number": "123456",
  "balance": 1000.0,
  "last_transaction": "2024-08-01T10:30:00.123456"
}
```

#### 2. Withdraw Money
```http
POST /accounts/{account_number}/withdraw
```

**Request Body:**
```json
{
  "amount": 200.0
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/accounts/123456/withdraw" \
     -H "Content-Type: application/json" \
     -d '{"amount": 200.0}'
```

**Example Response:**
```json
{
  "success": true,
  "message": "Withdrawal successful",
  "account_number": "123456",
  "previous_balance": 1000.0,
  "new_balance": 800.0,
  "transaction_amount": 200.0,
  "timestamp": "2024-08-01T10:35:00.123456"
}
```

#### 3. Deposit Money
```http
POST /accounts/{account_number}/deposit
```

**Request Body:**
```json
{
  "amount": 500.0
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/accounts/123456/deposit" \
     -H "Content-Type: application/json" \
     -d '{"amount": 500.0}'
```

**Example Response:**
```json
{
  "success": true,
  "message": "Deposit successful",
  "account_number": "123456", 
  "previous_balance": 800.0,
  "new_balance": 1300.0,
  "transaction_amount": 500.0,
  "timestamp": "2024-08-01T10:40:00.123456"
}
```

### Error Responses

#### Account Not Found (404)
```json
{
  "error": "Account Not Found",
  "detail": "Account 999999 not found",
  "account_number": "999999"
}
```

#### Insufficient Funds (400)
```json
{
  "error": "Insufficient Funds",
  "detail": "Insufficient funds. Balance: 100.0, Requested: 200.0",
  "current_balance": 100.0,
  "requested_amount": 200.0
}
```

#### Validation Error (422)
```json
{
  "error": "Validation Error",
  "detail": "Invalid input data",
  "errors": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

## 🧪 Testing

### Run All Tests (43 comprehensive tests)
```bash
# Run all tests with verbose output
pytest -v

# Quick test run
pytest -q

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Test Categories

#### 1. Account Operations (14 tests)
```bash
# Test balance operations
pytest tests/test_accounts.py::TestAccountBalance -v

# Test withdrawal operations  
pytest tests/test_accounts.py::TestWithdrawal -v

# Test deposit operations
pytest tests/test_accounts.py::TestDeposit -v

# Test transaction sequences
pytest tests/test_accounts.py::TestTransactionSequence -v
```

#### 2. Decimal Precision (13 tests)
```bash
# Test financial precision and security
pytest tests/test_decimal_precision.py -v

# Specific precision tests
pytest tests/test_decimal_precision.py::TestFinancialArithmetic -v
pytest tests/test_decimal_precision.py::TestFinancialSecurityScenarios -v
```

#### 3. Security Validation (12 tests)
```bash
# Test security features
pytest tests/test_security.py -v

# Specific security categories
pytest tests/test_security.py::TestSecurityValidation -v
pytest tests/test_security.py::TestInputSanitization -v
```

### Environment Verification
```bash
# Verify Docker compatibility
python verify_compatibility.py
```

### Test Results Summary
- ✅ **43/43 tests passing** (100% success rate)
- ✅ **Account Operations**: All CRUD operations working
- ✅ **Financial Precision**: Decimal arithmetic validated  
- ✅ **Security**: XSS prevention, input validation confirmed
- ✅ **Error Handling**: Proper exception management verified

## 🏗️ Architecture

### Project Structure
- **main.py** - FastAPI application setup and configuration
- **models.py** - Pydantic data models for request/response validation
- **database.py** - In-memory data storage and management
- **routers/accounts.py** - ATM endpoint implementations
- **exceptions.py** - Custom exception classes and handlers
- **tests/** - Comprehensive test suite

### Design Decisions

1. **Financial Precision** - Decimal-based arithmetic instead of floats to prevent rounding errors
2. **Pydantic v2** - Latest validation framework with enhanced type safety and performance
3. **In-Memory Storage** - Dictionary-based storage for demo purposes (easily replaceable with database)
4. **Exception Handling** - Custom exceptions with proper HTTP status codes and secure error messages
5. **Modular Architecture** - Separated concerns with clear file organization and dependency injection
6. **Comprehensive Testing** - 43 tests covering all scenarios, edge cases, and security vulnerabilities
7. **Docker Security** - Multi-stage builds with distroless runtime for minimal attack surface

### Security Features
- **Input Validation**: Strict Pydantic models with pattern matching
- **XSS Prevention**: JSON-only API with input sanitization
- **Path Validation**: Account number format enforcement (6-digit regex)
- **Error Security**: No sensitive information leakage in error responses
- **Financial Security**: Decimal precision prevents floating-point manipulation
- **Rate Limiting**: Built-in protection against excessive requests

### Validation Rules
- **Account Numbers**: Must be exactly 6 digits (pattern: `^\d{6}$`)
- **Withdrawal Amounts**: Must be positive and not exceed account balance
- **Deposit Amounts**: Must be positive with maximum 2 decimal places
- **Transaction Limits**: Individual transactions limited to $10,000
- **Balance Limits**: Account balances capped at $1,000,000
- **Precision**: All monetary values use Decimal with 2-decimal precision

## 🚀 Deployment

### 🐳 Docker Deployment (Recommended)

#### Standard Secure Deployment
```bash
# Build with hardened Dockerfile
docker build -t atm-system .

# Run with security constraints
docker run -p 8000:8000 atm-system
```

#### Ultra-Secure Deployment (Chainguard)
```bash
# Build with zero-vulnerability base image
docker build -f Dockerfile.secure -t atm-system-secure .

# Run with production security
docker-compose -f docker-compose.secure.yml up -d
```

#### Docker Security Features
- ✅ **Multi-stage builds** - Separates build and runtime environments
- ✅ **Distroless runtime** - Minimal attack surface (no shell, no package manager)
- ✅ **Non-root execution** - Runs as unprivileged user
- ✅ **Version pinning** - Exact Python 3.11.2 for consistency
- ✅ **Vulnerability scanning** - Integrated pip audit
- ✅ **Security policies** - Read-only filesystem, dropped capabilities

### 🌐 Cloud Deployment

#### Production-Ready Platforms
- **AWS ECS/Fargate** - Container orchestration with auto-scaling
- **Google Cloud Run** - Serverless container deployment
- **Azure Container Instances** - Managed container service
- **Railway** - Git-based auto-deployment
- **Render** - Container deployment with SSL
- **Heroku** - Container registry deployment

#### Environment Configuration
```bash
# Production environment variables
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO
export ALLOWED_HOSTS=your-domain.com,api.your-domain.com
```

### 📊 Monitoring & Health Checks

#### Built-in Health Monitoring
```bash
# Health check endpoint
curl http://localhost:8000/health

# API documentation availability
curl http://localhost:8000/docs

# OpenAPI schema validation
curl http://localhost:8000/openapi.json
```

#### Production Monitoring Setup
```yaml
# Docker Compose health check
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🔧 Development

### Adding New Features

1. **Create new models** in `models.py`
2. **Add business logic** to appropriate router
3. **Update exception handling** in `exceptions.py`
4. **Write tests** in `tests/` directory
5. **Update documentation**

### Environment Variables

For production deployment, consider these environment variables:
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `DEBUG` - Enable debug mode (default: False)

## 📋 Dependencies & Requirements

### Current Production Dependencies
```txt
fastapi==0.115.12        # Latest FastAPI with security patches
uvicorn[standard]==0.34.2 # High-performance ASGI server
pydantic==2.11.5         # Data validation with Pydantic v2
pytest==7.4.3           # Testing framework
httpx==0.25.2            # HTTP client for testing
pytest-asyncio==0.21.1  # Async testing support
```

### Version Compatibility Matrix
| Component | Development | Docker | Status |
|-----------|-------------|---------|---------|
| Python | 3.11.2 | 3.11.2 | ✅ Matched |
| FastAPI | 0.115.12 | 0.115.12 | ✅ Matched |
| Pydantic | 2.11.5 | 2.11.5 | ✅ Matched |
| Uvicorn | 0.34.2 | 0.34.2 | ✅ Matched |

### Security Dependencies
- **Decimal** - Financial precision (Python stdlib)
- **Typing** - Type safety enforcement (Python stdlib)  
- **Logging** - Security event logging (Python stdlib)
- **Pathlib** - Secure file handling (Python stdlib)

### Development Tools
```bash
# Install development dependencies
pip install pytest pytest-cov pytest-asyncio

# Code quality tools (optional)
pip install black isort flake8 mypy

# Security scanning (optional)  
pip install bandit safety
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
```
