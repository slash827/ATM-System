"""API endpoints for ATM operations"""
from fastapi import APIRouter, Path
from datetime import datetime

from models.schemas import (
    BalanceResponse, TransactionResponse, WithdrawRequest, DepositRequest,
    TransferRequest, TransferResponse, CreateTimeDepositRequest, 
    TimeDepositResponse, ListTimeDepositsResponse
)
from database.test_db import db
from core.exceptions import AccountNotFoundError, InsufficientFundsError

# Create router (like Django urls.py)
router = APIRouter(prefix="/accounts", tags=["ATM Operations"])

# Create a separate router for time deposits that don't need account prefix
time_deposits_router = APIRouter(prefix="/time-deposits", tags=["Time Deposits"])

# Test-only endpoint for resetting database state
@router.post("/test/reset", include_in_schema=False)
async def reset_test_database():
    """Reset test database - only for testing"""
    db.reset_test_data()
    return {"message": "Test database reset successfully"}

@router.get("/{account_number}/balance", response_model=BalanceResponse)
async def get_balance(account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")):
    """Get account balance"""
    try:
        account = db.get_account(account_number)
        return BalanceResponse(
            account_number=account.account_number,
            balance=account.balance,
            last_transaction=account.last_transaction
        )
    except ValueError:
        raise AccountNotFoundError(account_number)

@router.post("/{account_number}/deposit", response_model=TransactionResponse)
async def deposit_money(request: DepositRequest, account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")):
    """Deposit money to account"""
    try:
        # Get account
        account = db.get_account(account_number)
        
        # Perform deposit
        previous_balance = account.balance
        account.balance += request.amount
        account.last_transaction = datetime.now()
        
        # Update account in database
        db.update_account(account)
        
        return TransactionResponse(
            success=True,
            message="Deposit successful",
            account_number=account.account_number,
            previous_balance=previous_balance,
            new_balance=account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
        )
    except ValueError:
        raise AccountNotFoundError(account_number)

@router.post("/{account_number}/withdraw", response_model=TransactionResponse)
async def withdraw_money(request: WithdrawRequest, account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")):
    """Withdraw money from account"""
    try:
        # Get account
        account = db.get_account(account_number)
        
        # Check sufficient funds
        if account.balance < request.amount:
            raise InsufficientFundsError(account_number, account.balance, request.amount)
        
        # Perform withdrawal
        previous_balance = account.balance
        account.balance -= request.amount
        account.last_transaction = datetime.now()
        
        # Update account in database
        db.update_account(account)
        
        return TransactionResponse(
            success=True,
            message="Withdrawal successful",
            account_number=account.account_number,
            previous_balance=previous_balance,
            new_balance=account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
        )
    except ValueError:
        raise AccountNotFoundError(account_number)

@router.post("/{account_number}/transfer", response_model=TransferResponse)
async def transfer_money(request: TransferRequest, account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")):
    """Transfer money between accounts"""
    try:
        # Get both accounts
        sender = db.get_account(account_number)
        recipient = db.get_account(request.recipient_account)
        
        # Check sufficient funds
        if sender.balance < request.amount:
            raise InsufficientFundsError(account_number, sender.balance, request.amount)
        
        # Perform transfer
        sender.balance -= request.amount
        recipient.balance += request.amount
        sender.last_transaction = datetime.now()
        recipient.last_transaction = datetime.now()
        
        # Update both accounts
        db.update_account(sender)
        db.update_account(recipient)
        
        return TransferResponse(
            success=True,
            message="Transfer successful",
            sender_account=sender.account_number,
            recipient_account=recipient.account_number,
            sender_new_balance=sender.balance,
            recipient_new_balance=recipient.balance,
            transfer_amount=request.amount,
            timestamp=datetime.now()
        )
    except ValueError:
        raise AccountNotFoundError(account_number)

# Time deposit endpoints (simplified for now)
@time_deposits_router.post("/", response_model=TimeDepositResponse)
async def create_time_deposit(request: CreateTimeDepositRequest):
    """Create a time deposit"""
    try:
        # For now, return a simple success response
        return TimeDepositResponse(
            success=True,
            message="Time deposit feature not fully implemented in test mode",
            deposit_id="TD123456",
            account_number=request.account_number,
            amount=request.amount,
            duration_months=request.duration_months,
            interest_rate=0.025,
            maturity_date=datetime.now()
        )
    except ValueError:
        raise AccountNotFoundError(request.account_number)

@time_deposits_router.get("/{account_number}", response_model=ListTimeDepositsResponse)
async def list_time_deposits(account_number: str = Path(..., pattern=r"^\d{6}$")):
    """List time deposits for an account"""
    try:
        # Verify account exists
        db.get_account(account_number)
        
        return ListTimeDepositsResponse(
            account_number=account_number,
            deposits=[]  # Empty for test mode
        )
    except ValueError:
        raise AccountNotFoundError(account_number)
