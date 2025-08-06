"""
Unit tests for database operations
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

from backend.database.test_db import TestDatabase

class TestAccountDatabase:
    """Test TestDatabase operations"""
    
    @pytest.fixture
    def db(self):
        """Create a fresh database instance for each test"""
        db = TestDatabase()
        db.reset_test_data()
        return db
    
    def test_get_existing_account(self, db):
        """Test getting an existing account"""
        account = db.get_account("123456")
        assert account.account_number == "123456"
        assert account.balance >= 0
    
    def test_get_nonexistent_account(self, db):
        """Test getting a non-existent account raises error"""
        with pytest.raises(ValueError, match="Account 999999 not found"):
            db.get_account("999999")
    
    def test_update_account(self, db):
        """Test updating an account"""
        account = db.get_account("123456")
        original_balance = account.balance
        
        # Modify balance
        account.balance += Decimal("100.00")
        account.last_transaction = datetime.now()
        db.update_account(account)
        
        # Verify update
        updated_account = db.get_account("123456")
        assert updated_account.balance == original_balance + Decimal("100.00")
        assert updated_account.last_transaction is not None
    
    def test_reset_test_data(self, db):
        """Test that reset_test_data works correctly"""
        # Modify an account
        account = db.get_account("123456")
        account.balance = Decimal("999.99")
        db.update_account(account)
        
        # Reset
        db.reset_test_data()
        
        # Verify reset
        reset_account = db.get_account("123456")
        assert reset_account.balance == Decimal("1000.00")

# Time deposit functionality is not implemented in test database
# These tests are commented out for now

"""
class TestTimeDeposits:
    #Test time deposit operations - DISABLED for test database
    
    @pytest.fixture
    def db(self):
        #Create a fresh database instance for each test
        return TestDatabase()
"""
