from fastapi import APIRouter, Path
import sys
from pathlib import Path as FilePath

# Add parent directory to Python path for imports
parent_dir = FilePath(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from models import (
    BalanceResponse, TransactionResponse, WithdrawRequest, DepositRequest,
    TransferRequest, TransferResponse, CreateTimeDepositRequest, 
    TimeDepositResponse, ListTimeDepositsResponse
)
from database import db
from exceptions import AccountNotFoundError, InsufficientFundsError
from datetime import datetime

# Create router (like Django urls.py)
router = APIRouter(prefix="/accounts", tags=["ATM Operations"])

# Create a separate router for time deposits that don't need account prefix
time_deposits_router = APIRouter(prefix="/time-deposits", tags=["Time Deposits"])

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
        
        # Update database
        db.update_account(account)
        
        return TransactionResponse(
            success=True,
            message="Withdrawal successful",
            account_number=account_number,
            previous_balance=previous_balance,
            new_balance=account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
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
        
        # Update database
        db.update_account(account)
        
        return TransactionResponse(
            success=True,
            message="Deposit successful", 
            account_number=account_number,
            previous_balance=previous_balance,
            new_balance=account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
        )
    
    except ValueError:
        raise AccountNotFoundError(account_number)

# Debug endpoint
@router.get("/debug/all")
async def list_all_accounts():
    """Debug endpoint to see all accounts"""
    return {
        "total_accounts": len(db.accounts),
        "accounts": db.get_all_accounts()
    }

# Money Transfer Endpoints
@router.post("/{account_number}/transfer", response_model=TransferResponse)
async def transfer_money(
    request: TransferRequest, 
    account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit sender account number")
):
    """Transfer money from sender account to recipient account"""
    try:
        # Validate that sender and recipient are different
        if account_number == request.recipient_account:
            raise ValueError("Cannot transfer money to the same account")
        
        # Perform transfer
        sender, recipient = db.transfer_money(account_number, request.recipient_account, request.amount)
        
        return TransferResponse(
            success=True,
            message="Transfer successful",
            sender_account=account_number,
            recipient_account=request.recipient_account,
            sender_previous_balance=sender.balance + request.amount,  # Previous balance before transfer
            sender_new_balance=sender.balance,
            transfer_amount=request.amount,
            transfer_message=request.message,
            timestamp=datetime.now()
        )
    
    except ValueError as e:
        if "not found" in str(e):
            # Either sender or recipient account not found
            if account_number not in db.accounts:
                raise AccountNotFoundError(account_number)
            else:
                raise AccountNotFoundError(request.recipient_account)
        elif "Insufficient funds" in str(e):
            account = db.get_account(account_number)
            raise InsufficientFundsError(account_number, account.balance, request.amount)
        else:
            raise ValueError(str(e))

# Time Deposit Endpoints
@router.post("/{account_number}/time-deposits", response_model=TimeDepositResponse)
async def create_time_deposit(
    request: CreateTimeDepositRequest,
    account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")
):
    """Create a new time deposit"""
    try:
        # Create time deposit
        deposit = db.create_time_deposit(
            account_number, 
            request.amount, 
            request.duration_months,
            request.is_test_deposit
        )
        
        message = f"Time deposit created successfully. Deposit ID: {deposit.deposit_id}"
        if request.is_test_deposit:
            message += " (Test deposit - matures in 1 second)"
        
        return TimeDepositResponse(
            success=True,
            message=message,
            deposit=deposit
        )
    
    except ValueError as e:
        if "not found" in str(e):
            raise AccountNotFoundError(account_number)
        elif "Insufficient funds" in str(e):
            account = db.get_account(account_number)
            raise InsufficientFundsError(account_number, account.balance, request.amount)
        else:
            raise ValueError(str(e))

@router.get("/{account_number}/time-deposits", response_model=ListTimeDepositsResponse)
async def list_time_deposits(
    account_number: str = Path(..., pattern=r"^\d{6}$", description="6-digit account number")
):
    """List all time deposits for an account"""
    try:
        # Verify account exists
        db.get_account(account_number)
        
        # Get time deposits
        deposits = db.get_time_deposits(account_number)
        
        return ListTimeDepositsResponse(
            success=True,
            message=f"Found {len(deposits)} time deposits",
            deposits=deposits
        )
    
    except ValueError:
        raise AccountNotFoundError(account_number)

@time_deposits_router.post("/{deposit_id}/mature", response_model=TimeDepositResponse)
async def mature_time_deposit(
    deposit_id: str = Path(..., description="Time deposit ID"),
    force_mature: bool = False
):
    """Mature a time deposit and transfer funds back to account with interest"""
    try:
        # Mature the deposit
        deposit, final_amount = db.mature_time_deposit(deposit_id, force_mature)
        
        return TimeDepositResponse(
            success=True,
            message=f"Time deposit matured successfully. Final amount: ${final_amount:.2f}",
            deposit=deposit
        )
    
    except ValueError as e:
        if "not found" in str(e):
            raise ValueError(f"Time deposit {deposit_id} not found")
        else:
            raise ValueError(str(e))