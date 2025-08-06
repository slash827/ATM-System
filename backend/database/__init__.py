"""
Database interface for the ATM system
"""
from typing import Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from .postgresql import AccountModel, get_db, PostgreSQLAccountDatabase

class DatabaseInterface:
    """Unified database interface for the ATM system"""
    
    def __init__(self, db_session: Session):
        self.pg_db = PostgreSQLAccountDatabase(db_session)
    
    def get_account(self, account_number: str):
        """Get account by number - returns a simplified account object"""
        account_model = self.pg_db.get_account(account_number)
        return SimpleAccount(
            account_number=account_model.account_number,
            balance=account_model.balance,
            last_transaction=account_model.last_transaction
        )
    
    def update_account(self, account):
        """Update account balance"""
        # This method will be called by the API to persist changes
        # For PostgreSQL, we'll handle updates through specific transaction methods
        pass
    
    def deposit(self, account_number: str, amount: Decimal) -> tuple:
        """Perform deposit and return previous/new balance"""
        account_model = self.pg_db.get_account(account_number)
        previous_balance = account_model.balance
        new_balance = previous_balance + amount
        
        self.pg_db.update_account_balance(
            account_number=account_number,
            new_balance=new_balance,
            transaction_type="deposit",
            amount=amount,
            description="Deposit"
        )
        
        return previous_balance, new_balance
    
    def withdraw(self, account_number: str, amount: Decimal) -> tuple:
        """Perform withdrawal and return previous/new balance"""
        account_model = self.pg_db.get_account(account_number)
        previous_balance = account_model.balance
        
        if previous_balance < amount:
            from core.exceptions import InsufficientFundsError
            raise InsufficientFundsError(account_number, previous_balance, amount)
        
        new_balance = previous_balance - amount
        
        self.pg_db.update_account_balance(
            account_number=account_number,
            new_balance=new_balance,
            transaction_type="withdrawal",
            amount=amount,
            description="Withdrawal"
        )
        
        return previous_balance, new_balance

class SimpleAccount:
    """Simple account class to maintain compatibility with existing code"""
    
    def __init__(self, account_number: str, balance: Decimal, last_transaction: Optional[datetime]):
        self.account_number = account_number
        self.balance = balance
        self.last_transaction = last_transaction

# Global database instance placeholder
db = None

def get_database_interface(db_session: Session) -> DatabaseInterface:
    """Get database interface instance"""
    return DatabaseInterface(db_session)
