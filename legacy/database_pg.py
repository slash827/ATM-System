"""
Database configuration and models using SQLAlchemy with PostgreSQL support
"""
from sqlalchemy import create_engine, Column, String, DECIMAL, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import os
import uuid

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://postgres:password@localhost:5432/atm_system"
)

# For Railway deployment, handle the postgresql:// prefix that needs to be postgres://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Database Models
class AccountModel(Base):
    """SQLAlchemy model for accounts"""
    __tablename__ = "accounts"
    
    account_number = Column(String(6), primary_key=True, index=True)
    balance = Column(DECIMAL(15, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_transaction = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="active")
    
    # Relationships
    transactions = relationship("TransactionModel", back_populates="account")
    time_deposits = relationship("TimeDepositModel", back_populates="account")

class TransactionModel(Base):
    """SQLAlchemy model for transactions"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_number = Column(String(6), ForeignKey("accounts.account_number"), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # deposit, withdrawal, transfer_in, transfer_out
    amount = Column(DECIMAL(15, 2), nullable=False)
    balance_before = Column(DECIMAL(15, 2), nullable=False)
    balance_after = Column(DECIMAL(15, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="completed")
    description = Column(String(255), nullable=True)
    reference_id = Column(String(50), nullable=True)  # For transfers, this links related transactions
    
    # Relationships
    account = relationship("AccountModel", back_populates="transactions")

class TimeDepositModel(Base):
    """SQLAlchemy model for time deposits"""
    __tablename__ = "time_deposits"
    
    deposit_id = Column(String(8), primary_key=True, index=True)
    account_number = Column(String(6), ForeignKey("accounts.account_number"), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    duration_months = Column(Integer, nullable=False)
    interest_rate = Column(DECIMAL(5, 4), nullable=False)  # Store as decimal (e.g., 0.0250 for 2.5%)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    maturity_date = Column(DateTime(timezone=True), nullable=False)
    is_matured = Column(Boolean, default=False)
    matured_at = Column(DateTime(timezone=True), nullable=True)
    final_amount = Column(DECIMAL(15, 2), nullable=True)  # Amount after maturation
    
    # Relationships
    account = relationship("AccountModel", back_populates="time_deposits")

# Database dependency for FastAPI
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostgreSQLAccountDatabase:
    """PostgreSQL database implementation for accounts"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
        # Interest rates by duration (annual rates as decimals)
        self.interest_rates = {
            1: Decimal('0.01'),   # 1%
            3: Decimal('0.015'),  # 1.5%
            6: Decimal('0.02'),   # 2%
            12: Decimal('0.025'), # 2.5%
            24: Decimal('0.03'),  # 3%
            36: Decimal('0.035'), # 3.5%
            48: Decimal('0.04'),  # 4%
            60: Decimal('0.045'), # 4.5%
        }
    
    def get_account(self, account_number: str) -> Optional[AccountModel]:
        """Get account by number"""
        account = self.db.query(AccountModel).filter(AccountModel.account_number == account_number).first()
        if not account:
            raise ValueError(f"Account {account_number} not found")
        return account
    
    def create_account(self, account_number: str, initial_balance: Decimal = Decimal('0.00')) -> AccountModel:
        """Create a new account"""
        # Check if account already exists
        existing = self.db.query(AccountModel).filter(AccountModel.account_number == account_number).first()
        if existing:
            raise ValueError(f"Account {account_number} already exists")
        
        account = AccountModel(
            account_number=account_number,
            balance=initial_balance,
            created_at=datetime.now(),
            last_transaction=None
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update_account_balance(self, account_number: str, new_balance: Decimal, transaction_type: str, amount: Decimal, description: str = None) -> AccountModel:
        """Update account balance and create transaction record"""
        account = self.get_account(account_number)
        old_balance = account.balance
        
        # Update account
        account.balance = new_balance
        account.last_transaction = datetime.now()
        account.updated_at = datetime.now()
        
        # Create transaction record
        transaction = TransactionModel(
            account_number=account_number,
            transaction_type=transaction_type,
            amount=amount,
            balance_before=old_balance,
            balance_after=new_balance,
            timestamp=datetime.now(),
            description=description
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def account_exists(self, account_number: str) -> bool:
        """Check if account exists"""
        return self.db.query(AccountModel).filter(AccountModel.account_number == account_number).first() is not None
    
    def get_all_accounts(self) -> List[AccountModel]:
        """Get all accounts"""
        return self.db.query(AccountModel).all()
    
    # Money Transfer Methods
    def transfer_money(self, sender_account: str, recipient_account: str, amount: Decimal, description: str = None) -> tuple[AccountModel, AccountModel]:
        """Transfer money between accounts with atomic transaction"""
        # Get both accounts
        sender = self.get_account(sender_account)
        recipient = self.get_account(recipient_account)
        
        # Check sufficient funds
        if sender.balance < amount:
            raise ValueError(f"Insufficient funds in account {sender_account}")
        
        # Generate reference ID for linking transactions
        reference_id = str(uuid.uuid4())[:12]
        
        # Perform transfer with atomic transaction
        try:
            # Update sender
            new_sender_balance = sender.balance - amount
            sender.balance = new_sender_balance
            sender.last_transaction = datetime.now()
            sender.updated_at = datetime.now()
            
            # Update recipient
            new_recipient_balance = recipient.balance + amount
            recipient.balance = new_recipient_balance
            recipient.last_transaction = datetime.now()
            recipient.updated_at = datetime.now()
            
            # Create transaction records
            sender_transaction = TransactionModel(
                account_number=sender_account,
                transaction_type="transfer_out",
                amount=amount,
                balance_before=sender.balance + amount,  # Original balance
                balance_after=new_sender_balance,
                timestamp=datetime.now(),
                description=f"Transfer to {recipient_account}: {description}" if description else f"Transfer to {recipient_account}",
                reference_id=reference_id
            )
            
            recipient_transaction = TransactionModel(
                account_number=recipient_account,
                transaction_type="transfer_in",
                amount=amount,
                balance_before=recipient.balance - amount,  # Original balance
                balance_after=new_recipient_balance,
                timestamp=datetime.now(),
                description=f"Transfer from {sender_account}: {description}" if description else f"Transfer from {sender_account}",
                reference_id=reference_id
            )
            
            self.db.add(sender_transaction)
            self.db.add(recipient_transaction)
            self.db.commit()
            self.db.refresh(sender)
            self.db.refresh(recipient)
            
            return sender, recipient
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    # Time Deposit Methods
    def get_interest_rate(self, duration_months: int) -> Decimal:
        """Get interest rate for given duration"""
        available_durations = sorted(self.interest_rates.keys())
        for duration in available_durations:
            if duration_months <= duration:
                return self.interest_rates[duration]
        return self.interest_rates[max(available_durations)]
    
    def create_time_deposit(self, account_number: str, amount: Decimal, duration_months: int) -> TimeDepositModel:
        """Create a new time deposit"""
        # Verify account exists and has sufficient funds
        account = self.get_account(account_number)
        if account.balance < amount:
            raise ValueError(f"Insufficient funds in account {account_number}")
        
        # Generate unique deposit ID
        deposit_id = str(uuid.uuid4())[:8]
        
        # Calculate interest rate and maturity date
        interest_rate = self.get_interest_rate(duration_months)
        created_at = datetime.now()
        maturity_date = created_at + timedelta(days=duration_months * 30)
        
        try:
            # Deduct amount from account and create transaction
            self.update_account_balance(
                account_number=account_number,
                new_balance=account.balance - amount,
                transaction_type="time_deposit",
                amount=amount,
                description=f"Time deposit created: {deposit_id}"
            )
            
            # Create time deposit
            time_deposit = TimeDepositModel(
                deposit_id=deposit_id,
                account_number=account_number,
                amount=amount,
                duration_months=duration_months,
                interest_rate=interest_rate,
                created_at=created_at,
                maturity_date=maturity_date,
                is_matured=False
            )
            
            self.db.add(time_deposit)
            self.db.commit()
            self.db.refresh(time_deposit)
            
            return time_deposit
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_time_deposits(self, account_number: str) -> List[TimeDepositModel]:
        """Get all time deposits for an account"""
        return self.db.query(TimeDepositModel).filter(TimeDepositModel.account_number == account_number).all()
    
    def get_time_deposit(self, deposit_id: str) -> TimeDepositModel:
        """Get specific time deposit by ID"""
        deposit = self.db.query(TimeDepositModel).filter(TimeDepositModel.deposit_id == deposit_id).first()
        if not deposit:
            raise ValueError(f"Time deposit {deposit_id} not found")
        return deposit
    
    def mature_time_deposit(self, deposit_id: str) -> tuple[TimeDepositModel, Decimal]:
        """Mature a time deposit and calculate final amount with interest"""
        deposit = self.get_time_deposit(deposit_id)
        
        if deposit.is_matured:
            raise ValueError(f"Time deposit {deposit_id} is already matured")
        
        # Allow early maturation for testing, but in production you might want to enforce maturity date
        # if datetime.now() < deposit.maturity_date:
        #     raise ValueError(f"Time deposit {deposit_id} has not reached maturity date")
        
        try:
            # Calculate interest earned
            years = deposit.duration_months / 12
            interest_earned = deposit.amount * deposit.interest_rate * Decimal(str(years))
            final_amount = deposit.amount + interest_earned
            
            # Add money back to account with interest
            account = self.get_account(deposit.account_number)
            self.update_account_balance(
                account_number=deposit.account_number,
                new_balance=account.balance + final_amount,
                transaction_type="time_deposit_maturity",
                amount=final_amount,
                description=f"Time deposit matured: {deposit_id} (Principal: {deposit.amount}, Interest: {interest_earned})"
            )
            
            # Mark deposit as matured
            deposit.is_matured = True
            deposit.matured_at = datetime.now()
            deposit.final_amount = final_amount
            
            self.db.commit()
            self.db.refresh(deposit)
            
            return deposit, final_amount
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_transaction_history(self, account_number: str, limit: int = 50, offset: int = 0) -> List[TransactionModel]:
        """Get transaction history for an account"""
        return (self.db.query(TransactionModel)
                .filter(TransactionModel.account_number == account_number)
                .order_by(TransactionModel.timestamp.desc())
                .limit(limit)
                .offset(offset)
                .all())

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def seed_database():
    """Seed database with initial test accounts"""
    db = SessionLocal()
    try:
        # Check if accounts already exist
        existing_accounts = db.query(AccountModel).count()
        if existing_accounts > 0:
            print("Database already seeded")
            return
        
        # Create sample accounts
        accounts = [
            AccountModel(
                account_number="123456",
                balance=Decimal('1000.00'),
                created_at=datetime.now(),
                status="active"
            ),
            AccountModel(
                account_number="789012",
                balance=Decimal('500.00'),
                created_at=datetime.now(),
                status="active"
            ),
            AccountModel(
                account_number="555444",
                balance=Decimal('0.00'),
                created_at=datetime.now(),
                status="active"
            )
        ]
        
        for account in accounts:
            db.add(account)
        
        db.commit()
        print("Database seeded with sample accounts")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables and seed database
    create_tables()
    seed_database()
