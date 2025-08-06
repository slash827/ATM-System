from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
from pathlib import Path as FilePath

# Add parent directory to Python path for imports
parent_dir = FilePath(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from models import (
    BalanceResponse, TransactionResponse, WithdrawRequest, DepositRequest,
    TransferRequest, TransferResponse, CreateTimeDepositRequest, 
    TimeDepositResponse, ListTimeDepositsResponse, Account, TimeDeposit
)
from database_pg import get_db, PostgreSQLAccountDatabase, AccountModel, TimeDepositModel
from exceptions import AccountNotFoundError, InsufficientFundsError, InvalidAmountError
from datetime import datetime
from decimal import Decimal

# Create router (like Django urls.py)
router = APIRouter(prefix="/accounts", tags=["ATM Operations"])

def get_account_db(db: Session = Depends(get_db)) -> PostgreSQLAccountDatabase:
    """Get account database instance"""
    return PostgreSQLAccountDatabase(db)

@router.get("/{account_number}/balance", response_model=BalanceResponse)
async def get_balance(
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Get account balance"""
    try:
        account = account_db.get_account(account_number)
        return BalanceResponse(
            account_number=account.account_number,
            balance=account.balance,
            last_transaction=account.last_transaction
        )
    except ValueError:
        raise AccountNotFoundError()

@router.post("/{account_number}/withdraw", response_model=TransactionResponse)
async def withdraw_money(
    request: WithdrawRequest,
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Withdraw money from account"""
    try:
        account = account_db.get_account(account_number)
        
        # Check sufficient funds
        if account.balance < request.amount:
            raise InsufficientFundsError()
        
        # Perform withdrawal
        new_balance = account.balance - request.amount
        updated_account = account_db.update_account_balance(
            account_number=account_number,
            new_balance=new_balance,
            transaction_type="withdrawal",
            amount=request.amount,
            description="ATM withdrawal"
        )
        
        return TransactionResponse(
            success=True,
            message="Withdrawal successful",
            account_number=account_number,
            previous_balance=account.balance,
            new_balance=updated_account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
        )
        
    except ValueError:
        raise AccountNotFoundError()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

@router.post("/{account_number}/deposit", response_model=TransactionResponse)
async def deposit_money(
    request: DepositRequest,
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Deposit money to account"""
    try:
        account = account_db.get_account(account_number)
        
        # Perform deposit
        new_balance = account.balance + request.amount
        updated_account = account_db.update_account_balance(
            account_number=account_number,
            new_balance=new_balance,
            transaction_type="deposit",
            amount=request.amount,
            description="ATM deposit"
        )
        
        return TransactionResponse(
            success=True,
            message="Deposit successful",
            account_number=account_number,
            previous_balance=account.balance,
            new_balance=updated_account.balance,
            transaction_amount=request.amount,
            timestamp=datetime.now()
        )
        
    except ValueError:
        raise AccountNotFoundError()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

@router.post("/{sender_account}/transfer", response_model=TransferResponse)
async def transfer_money(
    request: TransferRequest,
    sender_account: str = Path(..., pattern=r"^\\d{6}$", description="6-digit sender account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Transfer money between accounts"""
    try:
        # Validate recipient account exists
        if not account_db.account_exists(request.recipient_account):
            raise AccountNotFoundError()
        
        # Perform transfer
        sender, recipient = account_db.transfer_money(
            sender_account=sender_account,
            recipient_account=request.recipient_account,
            amount=request.amount,
            description=request.message
        )
        
        return TransferResponse(
            success=True,
            message="Transfer successful",
            sender_account=sender_account,
            recipient_account=request.recipient_account,
            amount=request.amount,
            sender_new_balance=sender.balance,
            recipient_new_balance=recipient.balance,
            timestamp=datetime.now()
        )
        
    except ValueError as e:
        if "not found" in str(e):
            raise AccountNotFoundError()
        elif "Insufficient funds" in str(e):
            raise InsufficientFundsError()
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transfer failed: {str(e)}")

@router.post("/{account_number}/time-deposits", response_model=TimeDepositResponse)
async def create_time_deposit(
    request: CreateTimeDepositRequest,
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Create a time deposit"""
    try:
        # Create time deposit
        time_deposit = account_db.create_time_deposit(
            account_number=account_number,
            amount=request.amount,
            duration_months=request.duration_months
        )
        
        # Get updated account balance
        account = account_db.get_account(account_number)
        
        return TimeDepositResponse(
            success=True,
            message=f"Time deposit created successfully. Deposit ID: {time_deposit.deposit_id}",
            deposit_id=time_deposit.deposit_id,
            account_number=account_number,
            amount=time_deposit.amount,
            duration_months=time_deposit.duration_months,
            interest_rate=float(time_deposit.interest_rate),
            maturity_date=time_deposit.maturity_date,
            account_new_balance=account.balance,
            timestamp=time_deposit.created_at
        )
        
    except ValueError as e:
        if "not found" in str(e):
            raise AccountNotFoundError()
        elif "Insufficient funds" in str(e):
            raise InsufficientFundsError()
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Time deposit creation failed: {str(e)}")

@router.get("/{account_number}/time-deposits", response_model=ListTimeDepositsResponse)
async def get_time_deposits(
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Get all time deposits for an account"""
    try:
        # Verify account exists
        account_db.get_account(account_number)
        
        # Get time deposits
        deposits = account_db.get_time_deposits(account_number)
        
        # Convert to response models
        time_deposits = []
        for deposit in deposits:
            time_deposits.append(TimeDeposit(
                deposit_id=deposit.deposit_id,
                account_number=deposit.account_number,
                amount=deposit.amount,
                duration_months=deposit.duration_months,
                interest_rate=deposit.interest_rate,
                created_at=deposit.created_at,
                maturity_date=deposit.maturity_date,
                is_matured=deposit.is_matured,
                matured_at=deposit.matured_at,
                final_amount=deposit.final_amount
            ))
        
        return ListTimeDepositsResponse(
            account_number=account_number,
            time_deposits=time_deposits,
            total_deposits=len(time_deposits)
        )
        
    except ValueError:
        raise AccountNotFoundError()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get time deposits: {str(e)}")

@router.post("/time-deposits/{deposit_id}/mature", response_model=TimeDepositResponse)
async def mature_time_deposit(
    deposit_id: str = Path(..., description="Time deposit ID"),
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Mature a time deposit (for testing/admin purposes)"""
    try:
        # Mature the deposit
        deposit, final_amount = account_db.mature_time_deposit(deposit_id)
        
        # Get updated account balance
        account = account_db.get_account(deposit.account_number)
        
        return TimeDepositResponse(
            success=True,
            message=f"Time deposit {deposit_id} matured successfully. Final amount: ${final_amount}",
            deposit_id=deposit.deposit_id,
            account_number=deposit.account_number,
            amount=deposit.amount,
            duration_months=deposit.duration_months,
            interest_rate=float(deposit.interest_rate),
            maturity_date=deposit.maturity_date,
            account_new_balance=account.balance,
            timestamp=deposit.matured_at or datetime.now(),
            final_amount=final_amount
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Time deposit maturation failed: {str(e)}")

# Additional endpoints for PostgreSQL features

@router.get("/{account_number}/transactions")
async def get_transaction_history(
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    limit: int = 50,
    offset: int = 0,
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Get transaction history for an account"""
    try:
        # Verify account exists
        account_db.get_account(account_number)
        
        # Get transaction history
        transactions = account_db.get_transaction_history(account_number, limit, offset)
        
        return {
            "account_number": account_number,
            "transactions": [
                {
                    "id": t.id,
                    "type": t.transaction_type,
                    "amount": float(t.amount),
                    "balance_before": float(t.balance_before),
                    "balance_after": float(t.balance_after),
                    "timestamp": t.timestamp,
                    "description": t.description,
                    "reference_id": t.reference_id
                }
                for t in transactions
            ],
            "total_count": len(transactions),
            "limit": limit,
            "offset": offset
        }
        
    except ValueError:
        raise AccountNotFoundError()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get transaction history: {str(e)}")

@router.post("/{account_number}/create")
async def create_account(
    account_number: str = Path(..., pattern=r"^\\d{6}$", description="6-digit account number"),
    initial_balance: float = 0.0,
    account_db: PostgreSQLAccountDatabase = Depends(get_account_db)
):
    """Create a new account (admin endpoint)"""
    try:
        account = account_db.create_account(
            account_number=account_number,
            initial_balance=Decimal(str(initial_balance))
        )
        
        return {
            "success": True,
            "message": f"Account {account_number} created successfully",
            "account_number": account.account_number,
            "balance": float(account.balance),
            "created_at": account.created_at
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Account creation failed: {str(e)}")
