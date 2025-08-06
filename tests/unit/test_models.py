"""
Unit tests for account models and validation
"""
import pytest
from decimal import Decimal
from datetime import datetime
import sys
from pathlib import Path

# Add backend directory to path
project_root = Path(__file__).parent.parent.parent
backend_dir = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_dir))

from backend.models.schemas import (
    Account, TransactionRequest,
    CreateTimeDepositRequest
)

class TestAccountModel:
    """Test Account model validation"""
    
    def test_valid_account_creation(self):
        """Test creating a valid account"""
        account = Account(
            account_number="123456",
            balance=Decimal("1000.00"),
            created_at=datetime.now()
        )
        assert account.account_number == "123456"
        assert account.balance == Decimal("1000.00")
        assert account.last_transaction is None
    
    def test_invalid_account_number(self):
        """Test invalid account number formats"""
        with pytest.raises(ValueError):
            Account(
                account_number="12345",  # Too short
                balance=Decimal("1000.00"),
                created_at=datetime.now()
            )
        
        with pytest.raises(ValueError):
            Account(
                account_number="1234567",  # Too long
                balance=Decimal("1000.00"),
                created_at=datetime.now()
            )
    
    def test_negative_balance(self):
        """Test that negative balance is rejected"""
        with pytest.raises(ValueError):
            Account(
                account_number="123456",
                balance=Decimal("-100.00"),
                created_at=datetime.now()
            )
    
    def test_balance_precision(self):
        """Test balance decimal precision"""
        account = Account(
            account_number="123456",
            balance=1000.50,  # Should be converted to Decimal
            created_at=datetime.now()
        )
        assert isinstance(account.balance, Decimal)
        assert account.balance == Decimal("1000.50")

class TestTransactionRequests:
    """Test transaction request models"""
    
    def test_valid_transaction_request(self):
        """Test valid transaction request"""
        request = TransactionRequest(amount=Decimal("100.50"))
        assert request.amount == Decimal("100.50")
    
    def test_zero_amount_rejected(self):
        """Test that zero amount is rejected"""
        with pytest.raises(ValueError):
            TransactionRequest(amount=Decimal("0.00"))
    
    def test_negative_amount_rejected(self):
        """Test that negative amount is rejected"""
        with pytest.raises(ValueError):
            TransactionRequest(amount=Decimal("-50.00"))
    
    def test_amount_too_large(self):
        """Test that amounts over limit are rejected"""
        with pytest.raises(ValueError):
            TransactionRequest(amount=Decimal("20000.00"))
    
    def test_amount_precision_validation(self):
        """Test amount precision validation"""
        with pytest.raises(ValueError):
            TransactionRequest(amount=Decimal("100.123"))  # Too many decimal places

class TestTimeDepositRequest:
    """Test time deposit request model"""
    
    def test_valid_time_deposit_request(self):
        """Test valid time deposit request"""
        request = CreateTimeDepositRequest(
            amount=Decimal("1000.00"),
            duration_months=12,
            is_test_deposit=False
        )
        assert request.amount == Decimal("1000.00")
        assert request.duration_months == 12
        assert request.is_test_deposit is False
    
    def test_test_deposit_flag(self):
        """Test test deposit flag"""
        request = CreateTimeDepositRequest(
            amount=Decimal("100.00"),
            duration_months=3,
            is_test_deposit=True
        )
        assert request.is_test_deposit is True
    
    def test_invalid_duration(self):
        """Test invalid duration values"""
        with pytest.raises(ValueError):
            CreateTimeDepositRequest(
                amount=Decimal("1000.00"),
                duration_months=0  # Too short
            )
        
        with pytest.raises(ValueError):
            CreateTimeDepositRequest(
                amount=Decimal("1000.00"),
                duration_months=61  # Too long
            )
