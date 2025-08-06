# ATM System API

A robust, secure ATM (Automated Teller Machine) system built with FastAPI, featuring comprehensive financial operations, advanced security measures, and production-ready deployment. Includes both backend API and React frontend with PostgreSQL database support.

![Tests](https://img.shields.io/badge/tests-30%2B%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)
![React](https://img.shields.io/badge/React-18.3.1-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue)
![Security](https://img.shields.io/badge/Docker-Hardened-blue)

## 🏧 Features

### Core Banking Operations
- **Account Balance Inquiry** - Check current account balance with precise decimal handling
- **Money Withdrawal** - Secure withdrawals with balance validation and transaction logging
- **Money Deposit** - Fund deposits with amount validation and audit trails
- **Money Transfer** - Transfer funds between accounts with validation
- **Time Deposits** - Create and manage fixed-term deposits with interest calculation

### Frontend Application
- **React/TypeScript UI** - Modern, responsive web interface
- **Real-time Updates** - Live balance updates and transaction feedback
- **Dashboard** - Comprehensive account overview with quick actions
- **Responsive Design** - Mobile-friendly interface with Tailwind CSS
- **Error Handling** - User-friendly error messages and validation

### Security & Validation
- **Financial Precision** - Decimal-based arithmetic to avoid floating-point errors
- **Input Validation** - Comprehensive request validation with Pydantic v2
- **Security Hardening** - XSS prevention, input sanitization, and malicious input protection
- **Path Validation** - Account number format enforcement (6-digit pattern)
- **Error Handling** - Secure error responses without information leakage

### Development & Deployment
- **API Documentation** - Auto-generated interactive docs with OpenAPI 3.0
- **Comprehensive Testing** - 30+ tests covering all scenarios and edge cases
- **Docker Security** - Hardened multi-stage builds with distroless runtime
- **Production Ready** - Environment-based configuration and monitoring
- **Database Support** - SQLite for development, PostgreSQL for production

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
ATM-System/
├── backend/                    # Backend API (FastAPI)
│   ├── api/                   # API endpoints and routers
│   │   ├── accounts.py        # Account operations API
│   │   └── __init__.py
│   ├── core/                  # Core application components
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exception handlers
│   │   └── security.py        # Security utilities
│   ├── database/              # Database implementations
│   │   ├── postgresql.py      # PostgreSQL models and setup
│   │   ├── test_db.py         # Test database interface
│   │   └── __init__.py
│   ├── models/                # Data models and schemas
│   │   └── __init__.py
│   ├── utils/                 # Utility functions
│   ├── main.py                # FastAPI application entry point
│   └── test_config.py         # Test configuration
├── atm-frontend/              # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── pages/         # Page components (Dashboard, etc.)
│   │   │   └── ui/            # UI components (Button, Card, etc.)
│   │   ├── context/           # React context providers
│   │   ├── services/          # API service layer
│   │   ├── types/             # TypeScript type definitions
│   │   └── App.tsx            # Main React application
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite build configuration
├── tests/                     # Comprehensive test suite
│   ├── api/                   # API integration tests
│   ├── integration/           # System integration tests
│   ├── unit/                  # Unit tests
│   ├── test_accounts.py       # Account endpoint tests (14 tests)
│   ├── test_security.py       # Security validation tests (12 tests)
│   └── test_main.py           # Basic application tests (4 tests)
├── deployment/                # Deployment configurations
├── docs/                      # Project documentation
├── legacy/                    # Legacy files (for reference)
├── scripts/                   # Utility scripts
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Container configuration
└── README.md                  # Project documentation
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

5. **Run the backend server**
```bash
# Development mode with auto-reload
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or from project root
python -m backend.main
```

6. **Run the frontend (optional)**
```bash
cd atm-frontend
npm install
npm run dev
```

7. **Access the applications**
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend Alternative Docs**: http://localhost:8000/redoc
- **Backend Health Check**: http://localhost:8000/health
- **Frontend Application**: http://localhost:5173 (if running)

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

### Run All Tests (30+ comprehensive tests)
```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Quick test run
python -m pytest tests/ -q

# Run with coverage report
python -m pytest tests/ --cov=backend --cov-report=html
```

### Test Categories

#### 1. Account Operations (14 tests)
```bash
# Test balance operations
python -m pytest tests/test_accounts.py::TestAccountBalance -v

# Test withdrawal operations  
python -m pytest tests/test_accounts.py::TestWithdrawal -v

# Test deposit operations
python -m pytest tests/test_accounts.py::TestDeposit -v

# Test transaction sequences
python -m pytest tests/test_accounts.py::TestTransactionSequence -v
```

#### 2. Security Validation (12 tests)
```bash
# Test security features
python -m pytest tests/test_security.py -v

# Specific security categories
python -m pytest tests/test_security.py::TestSecurityValidation -v
python -m pytest tests/test_security.py::TestInputSanitization -v
```

#### 3. Integration Tests
```bash
# Test PostgreSQL setup
python -m pytest tests/integration/test_postgresql_setup.py -v

# Test frontend-backend integration  
python -m pytest tests/integration/test_frontend_backend.py -v
```

### Frontend Tests
```bash
# Run frontend tests
cd atm-frontend
npm test

# Run with coverage
npm run test:coverage
```

### Environment Verification
```bash
# Verify Docker compatibility
python verify_compatibility.py
```

### Test Results Summary
- ✅ **30+ tests passing** (100% success rate)
- ✅ **Account Operations**: All CRUD operations working
- ✅ **Security**: XSS prevention, input validation confirmed
- ✅ **Error Handling**: Proper exception management verified
- ✅ **Integration**: Frontend-backend communication tested

## 🏗️ Architecture

### Project Structure
- **backend/** - FastAPI application with organized modules
- **atm-frontend/** - React/TypeScript frontend application
- **tests/** - Comprehensive test suite organized by category
- **backend/api/** - RESTful API endpoints and business logic
- **backend/core/** - Core configuration, security, and exception handling
- **backend/database/** - Database implementations and models

### Design Decisions

1. **Modular Architecture** - Clean separation between frontend and backend
2. **Financial Precision** - Decimal-based arithmetic instead of floats to prevent rounding errors
3. **Database Flexibility** - Support for both SQLite (development) and PostgreSQL (production)
4. **Test Organization** - Structured test suite with proper isolation using API reset endpoints
5. **Exception Handling** - Custom exceptions with proper HTTP status codes and secure error messages
6. **Frontend Architecture** - Component-based React with TypeScript for type safety
7. **Security First** - Comprehensive input validation and XSS prevention
8. **Docker Ready** - Multi-stage builds with distroless runtime for minimal attack surface

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
# Backend Dependencies
fastapi==0.115.12        # Latest FastAPI with security patches
uvicorn[standard]==0.34.2 # High-performance ASGI server
pydantic==2.11.5         # Data validation with Pydantic v2
sqlalchemy==2.0.35       # ORM for database operations
psycopg2-binary==2.9.9   # PostgreSQL adapter
pytest==7.4.3           # Testing framework
httpx==0.25.2            # HTTP client for testing
pytest-asyncio==0.21.1  # Async testing support

# Frontend Dependencies  
react==18.3.1            # React framework
typescript==5.6.3        # TypeScript for type safety
vite==5.4.9              # Build tool and dev server
tailwindcss==3.4.17      # Utility-first CSS framework
```

### Version Compatibility Matrix
| Component | Development | Docker | Status |
|-----------|-------------|---------|---------|
| Python | 3.11.2 | 3.11.2 | ✅ Matched |
| FastAPI | 0.115.12 | 0.115.12 | ✅ Matched |
| Pydantic | 2.11.5 | 2.11.5 | ✅ Matched |
| PostgreSQL | 15+ | 15+ | ✅ Matched |
| Node.js | 18+ | 18+ | ✅ Matched |
| React | 18.3.1 | 18.3.1 | ✅ Matched |

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

## 👤 Author
- GitHub: [@slash827](https://github.com/slash827)
- Email: gilad.battat@gmail.com

---

**Built using FastAPI**
```