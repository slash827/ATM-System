from fastapi import APIRouter, Depends, Path
from models import BalanceResponse, TransactionResponse, WithdrawRequest, DepositRequest
from database import db
from exceptions import AccountNotFoundError, InsufficientFundsError, InvalidAmountError
from datetime import datetime

# Create router (like Django urls.py)
router = APIRouter(prefix="/accounts", tags=["ATM Operations"])

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