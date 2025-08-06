"""
Test database interface that provides the same API as the in-memory database
but uses proper test isolation and setup.
"""
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class Account:
    """Simple account class for testing"""
    account_number: str
    balance: Decimal
    last_transaction: Optional[datetime] = None

class TestDatabase:
    """Test database that provides proper test isolation"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestDatabase, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not TestDatabase._initialized:
            self.accounts: Dict[str, Account] = {}
            self._initialize_test_accounts()
            TestDatabase._initialized = True
    
    def _initialize_test_accounts(self):
        """Initialize test accounts"""
        self.accounts.clear()  # Clear existing accounts first
        self.accounts.update({
            "123456": Account("123456", Decimal("1000.00")),
            "789012": Account("789012", Decimal("500.00")),
            "555444": Account("555444", Decimal("0.00")),
        })
    
    def get_account(self, account_number: str) -> Account:
        """Get account by number"""
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} not found")
        return self.accounts[account_number]
    
    def update_account(self, account: Account):
        """Update account in database"""
        self.accounts[account.account_number] = account
    
    def reset_test_data(self):
        """Reset all accounts to initial test state"""
        # Instead of recreating the dictionary, update existing account objects
        if "123456" in self.accounts:
            self.accounts["123456"].balance = Decimal("1000.00")
            self.accounts["123456"].last_transaction = None
        else:
            self.accounts["123456"] = Account("123456", Decimal("1000.00"))
        
        if "789012" in self.accounts:
            self.accounts["789012"].balance = Decimal("500.00")
            self.accounts["789012"].last_transaction = None
        else:
            self.accounts["789012"] = Account("789012", Decimal("500.00"))
        
        if "555444" in self.accounts:
            self.accounts["555444"].balance = Decimal("0.00")
            self.accounts["555444"].last_transaction = None
        else:
            self.accounts["555444"] = Account("555444", Decimal("0.00"))

# Global test database instance (singleton)
db = TestDatabase()
