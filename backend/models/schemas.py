from pydantic import BaseModel, Field, field_validator, model_serializer
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

class Account(BaseModel):
    """Account data model with enhanced validation"""
    account_number: str = Field(..., pattern=r"^\d{6}$", description="6-digit account number")
    balance: Decimal = Field(ge=0, le=1000000, description="Account balance (0-1M)")
    created_at: datetime
    last_transaction: Optional[datetime] = None
    
    @field_validator('balance')
    @classmethod
    def convert_balance_to_decimal(cls, v):
        """Convert balance to Decimal with 2 decimal places"""
        if isinstance(v, (int, float)):
            return Decimal(str(v)).quantize(Decimal('0.01'))
        elif isinstance(v, Decimal):
            return v.quantize(Decimal('0.01'))
        return Decimal(str(v)).quantize(Decimal('0.01'))

class TransactionRequest(BaseModel):
    """Base model for transaction requests with strict validation"""
    amount: Decimal = Field(gt=0, le=10000, description="Transaction amount (0-10K per transaction)")
    
    @field_validator('amount')
    @classmethod
    def validate_amount_precision(cls, v):
        """Ensure amount has max 2 decimal places"""
        # Convert to Decimal and check precision
        decimal_v = Decimal(str(v))
        if decimal_v.as_tuple().exponent < -2:
            raise ValueError('Amount must have maximum 2 decimal places')
        return decimal_v.quantize(Decimal('0.01'))

class WithdrawRequest(TransactionRequest):
    """Request model for withdrawal operations"""
    pass

class DepositRequest(TransactionRequest):
    """Request model for deposit operations"""
    pass

# Response models remain the same but add validation
class BalanceResponse(BaseModel):
    """Response model for balance queries"""
    account_number: str = Field(..., pattern=r"^\d{6}$")
    balance: Decimal = Field(ge=0)
    last_transaction: Optional[datetime] = None
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        return {
            "account_number": self.account_number,
            "balance": float(self.balance),
            "last_transaction": self.last_transaction
        }

class TransactionResponse(BaseModel):
    """Response model for transaction operations"""
    success: bool
    message: str = Field(..., max_length=200)
    account_number: str = Field(..., pattern=r"^\d{6}$")
    previous_balance: Decimal = Field(ge=0)
    new_balance: Decimal = Field(ge=0)
    transaction_amount: Decimal = Field(gt=0)
    timestamp: datetime
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "account_number": self.account_number,
            "previous_balance": float(self.previous_balance),
            "new_balance": float(self.new_balance),
            "transaction_amount": float(self.transaction_amount),
            "timestamp": self.timestamp
        }

# Money Transfer Models
class TransferRequest(BaseModel):
    """Request model for money transfer operations"""
    amount: Decimal = Field(gt=0, le=10000, description="Transfer amount (0-10K per transfer)")
    recipient_account: str = Field(..., pattern=r"^\d{6}$", description="6-digit recipient account number")
    message: Optional[str] = Field(None, max_length=100, description="Optional transfer message")
    
    @field_validator('amount')
    @classmethod
    def validate_amount_precision(cls, v):
        """Ensure amount has max 2 decimal places"""
        decimal_v = Decimal(str(v))
        if decimal_v.as_tuple().exponent < -2:
            raise ValueError('Amount must have maximum 2 decimal places')
        return decimal_v.quantize(Decimal('0.01'))

class TransferResponse(BaseModel):
    """Response model for money transfer operations"""
    success: bool
    message: str = Field(..., max_length=200)
    sender_account: str = Field(..., pattern=r"^\d{6}$")
    recipient_account: str = Field(..., pattern=r"^\d{6}$")
    sender_previous_balance: Decimal = Field(ge=0)
    sender_new_balance: Decimal = Field(ge=0)
    transfer_amount: Decimal = Field(gt=0)
    transfer_message: Optional[str] = None
    timestamp: datetime
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "sender_account": self.sender_account,
            "recipient_account": self.recipient_account,
            "sender_previous_balance": float(self.sender_previous_balance),
            "sender_new_balance": float(self.sender_new_balance),
            "transfer_amount": float(self.transfer_amount),
            "transfer_message": self.transfer_message,
            "timestamp": self.timestamp
        }

# Time Deposit Models
class TimeDeposit(BaseModel):
    """Time deposit data model"""
    deposit_id: str = Field(..., description="Unique deposit identifier")
    account_number: str = Field(..., pattern=r"^\d{6}$", description="6-digit account number")
    amount: Decimal = Field(gt=0, description="Deposit amount")
    duration_months: int = Field(ge=1, le=60, description="Deposit duration in months (1-60)")
    interest_rate: Decimal = Field(ge=0, description="Annual interest rate as decimal")
    created_at: datetime
    maturity_date: datetime
    is_matured: bool = False
    
    @field_validator('amount')
    @classmethod
    def validate_amount_precision(cls, v):
        """Ensure amount has max 2 decimal places"""
        decimal_v = Decimal(str(v))
        if decimal_v.as_tuple().exponent < -2:
            raise ValueError('Amount must have maximum 2 decimal places')
        return decimal_v.quantize(Decimal('0.01'))

class CreateTimeDepositRequest(BaseModel):
    """Request model for creating time deposits"""
    amount: Decimal = Field(gt=0, le=100000, description="Deposit amount (0-100K per deposit)")
    duration_months: int = Field(ge=1, le=60, description="Deposit duration in months (1-60)")
    is_test_deposit: bool = Field(default=False, description="Whether this is a test deposit that matures in 1 second")
    
    @field_validator('amount')
    @classmethod
    def validate_amount_precision(cls, v):
        """Ensure amount has max 2 decimal places"""
        decimal_v = Decimal(str(v))
        if decimal_v.as_tuple().exponent < -2:
            raise ValueError('Amount must have maximum 2 decimal places')
        return decimal_v.quantize(Decimal('0.01'))

class TimeDepositResponse(BaseModel):
    """Response model for time deposit operations"""
    success: bool
    message: str = Field(..., max_length=200)
    deposit: Optional[TimeDeposit] = None
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        result = {
            "success": self.success,
            "message": self.message
        }
        if self.deposit:
            result["deposit"] = {
                "deposit_id": self.deposit.deposit_id,
                "account_number": self.deposit.account_number,
                "amount": float(self.deposit.amount),
                "duration_months": self.deposit.duration_months,
                "interest_rate": float(self.deposit.interest_rate),
                "created_at": self.deposit.created_at,
                "maturity_date": self.deposit.maturity_date,
                "is_matured": self.deposit.is_matured
            }
        return result

class ListTimeDepositsResponse(BaseModel):
    """Response model for listing time deposits"""
    success: bool
    message: str = Field(..., max_length=200)
    deposits: list[TimeDeposit] = []
    
    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "deposits": [
                {
                    "deposit_id": deposit.deposit_id,
                    "account_number": deposit.account_number,
                    "amount": float(deposit.amount),
                    "duration_months": deposit.duration_months,
                    "interest_rate": float(deposit.interest_rate),
                    "created_at": deposit.created_at,
                    "maturity_date": deposit.maturity_date,
                    "is_matured": deposit.is_matured
                }
                for deposit in self.deposits
            ]
        }