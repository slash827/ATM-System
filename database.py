from typing import Dict
from datetime import datetime
from decimal import Decimal
from models import Account

class AccountDatabase:
    """In-memory database for accounts implemented with a dictionary"""
    
    def __init__(self):
        # Initialize with sample accounts
        self.accounts: Dict[str, Account] = {
            "123456": Account(
                account_number="123456",
                balance=Decimal('1000.00'),
                created_at=datetime.now(),
                last_transaction=None
            ),
            "789012": Account(
                account_number="789012", 
                balance=Decimal('500.00'),
                created_at=datetime.now(),
                last_transaction=None
            ),
            "555444": Account(
                account_number="555444",
                balance=Decimal('0.00'),  # Empty account for testing
                created_at=datetime.now(),
                last_transaction=None
            )
        }
    
    def get_account(self, account_number: str) -> Account:
        """Get account by number"""
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} not found")
        account = self.accounts[account_number]
        # Ensure balance is always Decimal
        if not isinstance(account.balance, Decimal):
            account.balance = Decimal(str(account.balance)).quantize(Decimal('0.01'))
        return account
    
    def update_account(self, account: Account) -> None:
        """Update account in database"""
        account.last_transaction = datetime.now()
        self.accounts[account.account_number] = account
    
    def account_exists(self, account_number: str) -> bool:
        """Check if account exists"""
        return account_number in self.accounts
    
    def get_all_accounts(self) -> Dict[str, Account]:
        """Get all accounts (for debugging)"""
        return self.accounts

# Global database instance
db = AccountDatabase()