from fastapi.testclient import TestClient
from backend.test_config import test_app
from backend.database.test_db import db

class TestAccountBalance:
    """Test balance-related operations"""
    
    def test_get_balance_existing_account(self):
        """Test getting balance for existing account"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            response = client.get("/accounts/123456/balance")
            assert response.status_code == 200
            data = response.json()
            assert data["account_number"] == "123456"
            assert data["balance"] == 1000.0
            assert "last_transaction" in data
    
    def test_get_balance_nonexistent_account(self):
        """Test getting balance for non-existent account"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            response = client.get("/accounts/999999/balance")
            assert response.status_code == 404
            data = response.json()
            assert data["error"] == "Account Not Found"
            assert "999999" in data["detail"]

class TestWithdrawal:
    """Test withdrawal operations"""
    
    def test_successful_withdrawal(self):
        """Test successful withdrawal"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            withdrawal_data = {"amount": 200.0}
            response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["account_number"] == "123456"
            assert data["previous_balance"] == 1000.0
            assert data["new_balance"] == 800.0
            assert data["transaction_amount"] == 200.0
            assert "timestamp" in data
    
    def test_insufficient_funds_withdrawal(self):
        """Test withdrawal with insufficient funds"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            withdrawal_data = {"amount": 1500.0}  # More than balance
            response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
            
            assert response.status_code == 400
            data = response.json()
            assert data["error"] == "Insufficient Funds"
            assert data["current_balance"] == 1000.0
            assert data["requested_amount"] == 1500.0
    
    def test_negative_amount_withdrawal(self):
        """Test withdrawal with negative amount"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            withdrawal_data = {"amount": -100.0}
            response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
            
            assert response.status_code == 422  # Validation error
            data = response.json()
            assert data["error"] == "Validation Error"
    
    def test_zero_amount_withdrawal(self):
        """Test withdrawal with zero amount"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            withdrawal_data = {"amount": 0.0}
            response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
            
            assert response.status_code == 422  # Validation error
    
    def test_withdrawal_nonexistent_account(self):
        """Test withdrawal from non-existent account"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            withdrawal_data = {"amount": 100.0}
            response = client.post("/accounts/999999/withdraw", json=withdrawal_data)
            
            assert response.status_code == 404
            data = response.json()
            assert data["error"] == "Account Not Found"

class TestDeposit:
    """Test deposit operations"""
    
    def test_successful_deposit(self):
        """Test successful deposit"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            deposit_data = {"amount": 300.0}
            response = client.post("/accounts/123456/deposit", json=deposit_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["account_number"] == "123456"
            assert data["previous_balance"] == 1000.0
            assert data["new_balance"] == 1300.0
            assert data["transaction_amount"] == 300.0
    
    def test_large_deposit(self):
        """Test large deposit amount"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            deposit_data = {"amount": 10000.0}
            response = client.post("/accounts/123456/deposit", json=deposit_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["new_balance"] == 11000.0
    
    def test_negative_amount_deposit(self):
        """Test deposit with negative amount"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            deposit_data = {"amount": -100.0}
            response = client.post("/accounts/123456/deposit", json=deposit_data)
            
            assert response.status_code == 422  # Validation error
    
    def test_deposit_nonexistent_account(self):
        """Test deposit to non-existent account"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            deposit_data = {"amount": 100.0}
            response = client.post("/accounts/999999/deposit", json=deposit_data)
            
            assert response.status_code == 404

class TestTransactionSequence:
    """Test multiple transactions in sequence"""
    
    def test_deposit_then_withdraw(self):
        """Test deposit followed by withdrawal"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            # First deposit
            deposit_data = {"amount": 500.0}
            response = client.post("/accounts/123456/deposit", json=deposit_data)
            assert response.status_code == 200
            assert response.json()["new_balance"] == 1500.0
            
            # Then withdraw
            withdrawal_data = {"amount": 200.0}
            response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
            assert response.status_code == 200
            assert response.json()["new_balance"] == 1300.0
    
    def test_multiple_small_withdrawals(self):
        """Test multiple small withdrawals"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            for i in range(5):
                withdrawal_data = {"amount": 100.0}
                response = client.post("/accounts/123456/withdraw", json=withdrawal_data)
                assert response.status_code == 200
                expected_balance = 1000.0 - (100.0 * (i + 1))
                assert response.json()["new_balance"] == expected_balance
    
    def test_empty_account_scenario(self):
        """Test operations on empty account"""
        with TestClient(test_app, raise_server_exceptions=False) as client:
            client.post("/accounts/test/reset")  # Reset database
            # Use empty account
            response = client.get("/accounts/555444/balance")
            assert response.json()["balance"] == 0.0
            
            # Try to withdraw from empty account
            withdrawal_data = {"amount": 10.0}
            response = client.post("/accounts/555444/withdraw", json=withdrawal_data)
            assert response.status_code == 400  # Insufficient funds
            
            # Deposit to empty account
            deposit_data = {"amount": 250.0}
            response = client.post("/accounts/555444/deposit", json=deposit_data)
            assert response.status_code == 200
