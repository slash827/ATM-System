from typing import Dict, List
from datetime import datetime, timedelta
from decimal import Decimal
from models import Account, TimeDeposit
import uuid

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
        
        # Initialize time deposits storage
        self.time_deposits: Dict[str, TimeDeposit] = {}
        
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
    
    # Money Transfer Methods
    def transfer_money(self, sender_account: str, recipient_account: str, amount: Decimal) -> tuple[Account, Account]:
        """Transfer money between accounts"""
        # Get both accounts
        sender = self.get_account(sender_account)
        recipient = self.get_account(recipient_account)
        
        # Check sufficient funds
        if sender.balance < amount:
            raise ValueError(f"Insufficient funds in account {sender_account}")
        
        # Perform transfer
        sender.balance -= amount
        recipient.balance += amount
        
        # Update both accounts
        self.update_account(sender)
        self.update_account(recipient)
        
        return sender, recipient
    
    # Time Deposit Methods
    def get_interest_rate(self, duration_months: int) -> Decimal:
        """Get interest rate for given duration"""
        # Find the closest duration with interest rate
        available_durations = sorted(self.interest_rates.keys())
        for duration in available_durations:
            if duration_months <= duration:
                return self.interest_rates[duration]
        
        # If duration is longer than highest tier, use highest rate
        return self.interest_rates[max(available_durations)]
    
    def create_time_deposit(self, account_number: str, amount: Decimal, duration_months: int, is_test_deposit: bool = False) -> TimeDeposit:
        """Create a new time deposit"""
        # Verify account exists and has sufficient funds
        account = self.get_account(account_number)
        if account.balance < amount:
            raise ValueError(f"Insufficient funds in account {account_number}")
        
        # Deduct amount from account
        account.balance -= amount
        self.update_account(account)
        
        # Generate unique deposit ID
        deposit_id = str(uuid.uuid4())[:8]
        
        # Calculate interest rate and maturity date
        interest_rate = self.get_interest_rate(duration_months)
        created_at = datetime.now()
        
        # For test deposits, set maturity to 1 second from now
        if is_test_deposit:
            maturity_date = created_at + timedelta(seconds=1)
        else:
            maturity_date = created_at + timedelta(days=duration_months * 30)  # Approximate
        
        # Create time deposit
        time_deposit = TimeDeposit(
            deposit_id=deposit_id,
            account_number=account_number,
            amount=amount,
            duration_months=duration_months,
            interest_rate=interest_rate,
            created_at=created_at,
            maturity_date=maturity_date,
            is_matured=False
        )
        
        # Store in database
        self.time_deposits[deposit_id] = time_deposit
        
        return time_deposit
    
    def get_time_deposits(self, account_number: str) -> List[TimeDeposit]:
        """Get all time deposits for an account"""
        return [
            deposit for deposit in self.time_deposits.values()
            if deposit.account_number == account_number
        ]
    
    def get_time_deposit(self, deposit_id: str) -> TimeDeposit:
        """Get specific time deposit by ID"""
        if deposit_id not in self.time_deposits:
            raise ValueError(f"Time deposit {deposit_id} not found")
        return self.time_deposits[deposit_id]
    
    def mature_time_deposit(self, deposit_id: str, force_mature: bool = False) -> tuple[TimeDeposit, Decimal]:
        """Mature a time deposit and calculate final amount with interest"""
        deposit = self.get_time_deposit(deposit_id)
        
        if deposit.is_matured:
            raise ValueError(f"Time deposit {deposit_id} is already matured")
        
        # Check if deposit has reached maturity (or force mature for testing)
        if not force_mature and datetime.now() < deposit.maturity_date:
            raise ValueError(f"Time deposit {deposit_id} has not reached maturity date")
        
        # Calculate interest earned
        years = deposit.duration_months / 12
        interest_earned = deposit.amount * deposit.interest_rate * Decimal(str(years))
        final_amount = deposit.amount + interest_earned
        
        # Add money back to account with interest
        account = self.get_account(deposit.account_number)
        account.balance += final_amount
        self.update_account(account)
        
        # Mark deposit as matured
        deposit.is_matured = True
        self.time_deposits[deposit_id] = deposit
        
        return deposit, final_amount

# Global database instance
db = AccountDatabase()