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