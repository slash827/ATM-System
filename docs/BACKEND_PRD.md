# ATM System Backend API - Product Requirements Document (PRD)

## 1. Project Overview

### 1.1 Purpose
Develop a secure, robust RESTful API for an ATM (Automated Teller Machine) system that handles core banking operations including account management, balance inquiries, cash withdrawals, and deposits with enterprise-grade security and reliability.

### 1.2 Business Objectives
- **Digital Banking**: Provide modern API-first banking infrastructure
- **Security**: Implement banking-grade security standards
- **Scalability**: Support high-volume concurrent transactions
- **Compliance**: Ensure financial data accuracy and audit trails
- **Developer Experience**: Provide comprehensive API documentation

### 1.3 Success Metrics
- **Performance**: < 200ms API response time for 95% of requests
- **Reliability**: 99.9% uptime SLA
- **Security**: Zero data breaches, comprehensive audit logging
- **Accuracy**: 100% financial calculation precision using Decimal arithmetic
- **Documentation**: Complete OpenAPI/Swagger documentation

## 2. Functional Requirements

### 2.1 Core Banking Operations

#### FR1: Account Balance Inquiry
**Requirement**: Users must be able to check their current account balance
- **Input**: Valid 6-digit account number
- **Output**: Current account balance with precision to 2 decimal places
- **Validation**: Account number format validation, account existence verification
- **Error Handling**: Account not found, invalid format errors

#### FR2: Cash Withdrawal
**Requirement**: Users must be able to withdraw funds from their account
- **Input**: Account number, withdrawal amount
- **Output**: Updated balance, transaction confirmation
- **Business Rules**:
  - Withdrawal amount must be positive
  - Sufficient funds must be available
  - Maximum withdrawal limit enforcement (if applicable)
- **Validation**: Amount format, sufficient funds check
- **Error Handling**: Insufficient funds, invalid amount, account not found

#### FR3: Cash Deposit
**Requirement**: Users must be able to deposit funds into their account
- **Input**: Account number, deposit amount
- **Output**: Updated balance, transaction confirmation
- **Business Rules**:
  - Deposit amount must be positive
  - No maximum deposit limit (configurable)
- **Validation**: Amount format validation
- **Error Handling**: Invalid amount, account not found

### 2.2 Data Management

#### FR4: Account Data Model
```python
Account Entity:
- account_number: String (6 digits, unique identifier)
- balance: Decimal (precise to 2 decimal places)
- created_at: DateTime
- updated_at: DateTime
- status: Enum (active, inactive, frozen)
```

#### FR5: Transaction Logging
- **Requirement**: All transactions must be logged for audit purposes
- **Data**: Transaction ID, account number, operation type, amount, timestamp, status
- **Retention**: Configurable retention period for compliance

### 2.3 API Specifications

#### FR6: REST API Endpoints
```
GET /accounts/{account_number}/balance
- Description: Retrieve account balance
- Parameters: account_number (path parameter)
- Response: {"balance": Decimal}

POST /accounts/{account_number}/withdraw
- Description: Withdraw funds from account
- Parameters: account_number (path), amount (body)
- Request Body: {"amount": Decimal}
- Response: {"new_balance": Decimal, "message": String}

POST /accounts/{account_number}/deposit
- Description: Deposit funds to account
- Parameters: account_number (path), amount (body)
- Request Body: {"amount": Decimal}
- Response: {"new_balance": Decimal, "message": String}

GET /health
- Description: Health check endpoint
- Response: {"status": "healthy", "timestamp": DateTime}

GET / 
- Description: Root endpoint with API information
- Response: {"message": String}
```

## 3. Non-Functional Requirements

### 3.1 Performance Requirements
- **Response Time**: 95% of API calls respond within 200ms
- **Throughput**: Support 1000+ concurrent requests
- **Scalability**: Horizontal scaling capability
- **Load Testing**: Handle 10,000 requests per minute

### 3.2 Security Requirements

#### NFR1: Input Validation
- **Pydantic Models**: Comprehensive request/response validation
- **SQL Injection Prevention**: Parameterized queries, ORM usage
- **XSS Protection**: Input sanitization and output encoding
- **Rate Limiting**: Protection against excessive requests

#### NFR2: Data Security
- **Encryption**: HTTPS enforcement for all communications
- **Data Validation**: Server-side validation for all inputs
- **Error Handling**: Sanitized error messages (no sensitive data exposure)
- **Audit Logging**: Comprehensive transaction and access logging

#### NFR3: Infrastructure Security
- **CORS Configuration**: Restricted origins for production
- **Trusted Host Middleware**: Host header validation
- **Environment Isolation**: Separate dev/staging/production configurations
- **Secrets Management**: Environment variable based configuration

### 3.3 Reliability Requirements
- **Error Handling**: Graceful degradation and meaningful error messages
- **Data Consistency**: ACID transaction properties
- **Backup Strategy**: Regular database backups
- **Monitoring**: Health checks and performance metrics

### 3.4 Compliance Requirements
- **Financial Precision**: Decimal arithmetic for all monetary calculations
- **Audit Trail**: Complete transaction history with timestamps
- **Data Retention**: Configurable retention policies
- **Documentation**: Complete API documentation for auditors

## 4. Technical Architecture

### 4.1 Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic v2 for data models
- **Testing**: Pytest with comprehensive test coverage
- **Documentation**: Automatic OpenAPI/Swagger generation
- **Deployment**: Docker containerization with Railway hosting

### 4.2 Application Structure
```
/
├── main.py                 # FastAPI application entry point
├── models.py              # Pydantic data models
├── database.py            # Database configuration and models
├── config.py              # Application configuration
├── security.py            # Security utilities and middleware
├── exceptions.py          # Custom exception handlers
├── routers/
│   └── accounts.py        # Account-related endpoints
├── tests/                 # Comprehensive test suite
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
└── README.md             # Project documentation
```

### 4.3 Database Schema
```sql
CREATE TABLE accounts (
    account_number VARCHAR(6) PRIMARY KEY,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number VARCHAR(6) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    balance_before DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed',
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);
```

## 5. Data Models & Validation

### 5.1 Request/Response Models
```python
# Request Models
class WithdrawRequest(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)

class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)

# Response Models
class BalanceResponse(BaseModel):
    balance: Decimal

class TransactionResponse(BaseModel):
    new_balance: Decimal
    message: str
    transaction_id: Optional[str] = None

# Error Models
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime
```

### 5.2 Validation Rules
- **Account Number**: Exactly 6 digits, numeric only
- **Amount**: Positive decimal, maximum 2 decimal places
- **Currency**: USD with precise decimal handling
- **Request Size**: Limited to prevent DoS attacks

## 6. Error Handling & Status Codes

### 6.1 HTTP Status Codes
- **200 OK**: Successful operations
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Account not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: System errors

### 6.2 Custom Exceptions
```python
class AccountNotFoundError(HTTPException):
    status_code = 404
    detail = "Account not found"

class InsufficientFundsError(HTTPException):
    status_code = 400
    detail = "Insufficient funds for this transaction"

class InvalidAmountError(HTTPException):
    status_code = 400
    detail = "Invalid amount specified"
```

## 7. Testing Strategy

### 7.1 Test Coverage Requirements
- **Unit Tests**: 90%+ code coverage
- **Integration Tests**: API endpoint testing
- **Performance Tests**: Load and stress testing
- **Security Tests**: Input validation and SQL injection testing

### 7.2 Test Categories
```
tests/
├── test_main.py           # Main application tests (4 tests)
├── test_accounts.py       # Account operations tests (14 tests)
├── test_security.py       # Security and validation tests (11 tests)
└── test_decimal_precision.py # Financial precision tests (14 tests)
```

### 7.3 Test Data
- **Mock Accounts**: Predefined test accounts with various balances
- **Edge Cases**: Zero balances, maximum amounts, invalid inputs
- **Error Scenarios**: Account not found, insufficient funds, invalid data

## 8. Deployment & Operations

### 8.1 Environment Configuration
```python
# Development
DEBUG = True
DATABASE_URL = "sqlite:///./test.db"
CORS_ORIGINS = ["http://localhost:3000"]

# Production  
DEBUG = False
DATABASE_URL = "production_database_url"
CORS_ORIGINS = []  # Restricted origins
```

### 8.2 Deployment Strategy
- **Containerization**: Docker with multi-stage builds
- **Cloud Platform**: Railway for automatic deployments
- **Environment Variables**: Configuration via environment
- **Health Checks**: Kubernetes-ready health endpoints

### 8.3 Monitoring & Logging
- **Structured Logging**: JSON formatted logs with correlation IDs
- **Metrics**: Response times, error rates, transaction volumes
- **Alerts**: Critical error notifications
- **Performance Monitoring**: APM integration

## 9. Security Implementation

### 9.1 Input Validation
```python
# Pydantic models with strict validation
class WithdrawRequest(BaseModel):
    amount: Decimal = Field(gt=0, le=10000, decimal_places=2)
    
    @validator('amount')
    def validate_amount_precision(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
```

### 9.2 Middleware Stack
```python
# Security middleware configuration
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(CORSMiddleware, 
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

## 10. API Documentation

### 10.1 OpenAPI/Swagger
- **Automatic Generation**: FastAPI auto-generates OpenAPI spec
- **Interactive Docs**: Swagger UI at `/docs` endpoint
- **ReDoc**: Alternative documentation at `/redoc`
- **Schema Export**: Downloadable OpenAPI JSON/YAML

### 10.2 Documentation Requirements
- **Endpoint Descriptions**: Clear operation summaries
- **Request Examples**: Sample JSON payloads
- **Response Examples**: Success and error responses
- **Authentication**: Future authentication requirements

## 11. Migration & Pydantic v2

### 11.1 Pydantic v2 Migration
- **BaseModel**: Updated to Pydantic v2 syntax
- **Field Validation**: Enhanced with Field() constraints
- **Decimal Handling**: Improved precision with decimal_places parameter
- **Performance**: 5-50x performance improvements

### 11.2 Before/After Examples
```python
# Pydantic v1 (Before)
class WithdrawRequest(BaseModel):
    amount: float
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('must be positive')
        return v

# Pydantic v2 (After)  
class WithdrawRequest(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)
```

## 12. Future Enhancements

### 12.1 Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- PIN/Password verification
- Session management

### 12.2 Advanced Features
- Transaction history endpoints
- Account statements generation
- Transfer between accounts
- Account management (create/close accounts)
- Real-time notifications
- Fraud detection algorithms

### 12.3 Operational Improvements
- Database connection pooling
- Caching layer (Redis)
- Message queues for async processing
- Microservices architecture
- Advanced monitoring and alerting

---

**Document Version**: 1.0  
**Created**: August 4, 2025  
**Target Completion**: 4 weeks from project start  
**Review Cycle**: Weekly during development
