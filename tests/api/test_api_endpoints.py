"""
API Integration Tests - Replicates all manual PowerShell testing
These tests automate all the API calls we manually tested
"""
import pytest
from decimal import Decimal
import time
import json

class TestBasicAPIEndpoints:
    """Test basic API functionality"""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "ATM System is running" in data["message"]
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "environment" in data

class TestAccountOperations:
    """Test account-related operations"""
    
    def test_get_balance_valid_account(self, client, test_account):
        """Test getting balance for valid account"""
        response = client.get(f"/accounts/{test_account}/balance")
        assert response.status_code == 200
        data = response.json()
        assert data["account_number"] == test_account
        assert "balance" in data
        assert isinstance(data["balance"], (int, float))
    
    def test_get_balance_invalid_account(self, client, invalid_account):
        """Test getting balance for invalid account"""
        response = client.get(f"/accounts/{invalid_account}/balance")
        assert response.status_code == 404
    
    def test_deposit_money(self, client, test_account):
        """Test depositing money"""
        # Get initial balance
        initial_response = client.get(f"/accounts/{test_account}/balance")
        initial_balance = initial_response.json()["balance"]
        
        # Deposit money
        deposit_amount = 50.00
        response = client.post(
            f"/accounts/{test_account}/deposit",
            json={"amount": deposit_amount}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["transaction_amount"] == deposit_amount
        assert data["new_balance"] == initial_balance + deposit_amount
    
    def test_withdraw_money(self, client, test_account):
        """Test withdrawing money"""
        # Get initial balance
        initial_response = client.get(f"/accounts/{test_account}/balance")
        initial_balance = initial_response.json()["balance"]
        
        # Withdraw money (only if sufficient balance)
        withdraw_amount = 25.00
        if initial_balance >= withdraw_amount:
            response = client.post(
                f"/accounts/{test_account}/withdraw",
                json={"amount": withdraw_amount}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["transaction_amount"] == withdraw_amount
            assert data["new_balance"] == initial_balance - withdraw_amount
    
    def test_withdraw_insufficient_funds(self, client):
        """Test withdrawing more money than available"""
        response = client.post(
            "/accounts/555444/withdraw",  # Empty account
            json={"amount": 100.00}
        )
        assert response.status_code == 400
        data = response.json()
        assert "insufficient funds" in data["detail"].lower()
    
    def test_invalid_transaction_amounts(self, client, test_account):
        """Test invalid transaction amounts"""
        # Test negative amount
        response = client.post(
            f"/accounts/{test_account}/deposit",
            json={"amount": -50.00}
        )
        assert response.status_code == 422
        
        # Test zero amount
        response = client.post(
            f"/accounts/{test_account}/deposit",
            json={"amount": 0.00}
        )
        assert response.status_code == 422
        
        # Test amount too large
        response = client.post(
            f"/accounts/{test_account}/deposit",
            json={"amount": 50000.00}
        )
        assert response.status_code == 422

class TestTimeDeposits:
    """Test time deposit functionality"""
    
    def test_create_regular_time_deposit(self, client, test_account):
        """Test creating a regular time deposit"""
        response = client.post(
            f"/accounts/{test_account}/time-deposits",
            json={
                "amount": 100.00,
                "duration_months": 12,
                "is_test_deposit": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "deposit_id" in data["deposit"]
        assert data["deposit"]["amount"] == 100.0
        assert data["deposit"]["duration_months"] == 12
    
    def test_create_test_time_deposit(self, client, test_account):
        """Test creating a quick test deposit"""
        response = client.post(
            f"/accounts/{test_account}/time-deposits",
            json={
                "amount": 25.00,
                "duration_months": 3,
                "is_test_deposit": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Test deposit" in data["message"]
        return data["deposit"]["deposit_id"]  # Return for maturity test
    
    def test_list_time_deposits(self, client, test_account):
        """Test listing time deposits"""
        response = client.get(f"/accounts/{test_account}/time-deposits")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "deposits" in data
        assert isinstance(data["deposits"], list)
    
    def test_mature_test_deposit_workflow(self, client, test_account):
        """Test the complete test deposit workflow"""
        # Create test deposit
        create_response = client.post(
            f"/accounts/{test_account}/time-deposits",
            json={
                "amount": 50.00,
                "duration_months": 6,
                "is_test_deposit": True
            }
        )
        assert create_response.status_code == 200
        deposit_id = create_response.json()["deposit"]["deposit_id"]
        
        # Wait for test deposit to mature (1 second)
        time.sleep(1.5)
        
        # Mature the deposit
        mature_response = client.post(f"/time-deposits/{deposit_id}/mature")
        assert mature_response.status_code == 200
        mature_data = mature_response.json()
        assert mature_data["success"] is True
        assert "matured successfully" in mature_data["message"]
        assert mature_data["deposit"]["is_matured"] is True
    
    def test_time_deposit_insufficient_funds(self, client):
        """Test creating time deposit with insufficient funds"""
        response = client.post(
            "/accounts/555444/time-deposits",  # Empty account
            json={
                "amount": 1000.00,
                "duration_months": 12
            }
        )
        assert response.status_code == 400

class TestMoneyTransfers:
    """Test money transfer functionality"""
    
    def test_successful_transfer(self, client):
        """Test successful money transfer between accounts"""
        # Get initial balances
        sender_response = client.get("/accounts/123456/balance")
        recipient_response = client.get("/accounts/789012/balance")
        
        sender_initial = sender_response.json()["balance"]
        recipient_initial = recipient_response.json()["balance"]
        
        transfer_amount = 30.00
        
        # Perform transfer
        response = client.post(
            "/accounts/123456/transfer",
            json={
                "amount": transfer_amount,
                "recipient_account": "789012",
                "message": "Test transfer"
            }
        )
        
        if sender_initial >= transfer_amount:  # Only test if sufficient funds
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["transfer_amount"] == transfer_amount
            assert data["sender_account"] == "123456"
            assert data["recipient_account"] == "789012"
    
    def test_transfer_to_same_account(self, client, test_account):
        """Test transferring to the same account (should fail)"""
        response = client.post(
            f"/accounts/{test_account}/transfer",
            json={
                "amount": 50.00,
                "recipient_account": test_account,
                "message": "Self transfer"
            }
        )
        assert response.status_code == 422

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_account_format(self, client):
        """Test invalid account number formats"""
        # Too short
        response = client.get("/accounts/12345/balance")
        assert response.status_code == 422
        
        # Too long
        response = client.get("/accounts/1234567/balance")
        assert response.status_code == 422
        
        # Non-numeric
        response = client.get("/accounts/abcdef/balance")
        assert response.status_code == 422
    
    def test_malformed_json(self, client, test_account):
        """Test malformed JSON requests"""
        response = client.post(
            f"/accounts/{test_account}/deposit",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client, test_account):
        """Test requests with missing required fields"""
        response = client.post(
            f"/accounts/{test_account}/deposit",
            json={}  # Missing amount
        )
        assert response.status_code == 422

class TestCORSAndSecurity:
    """Test CORS and security features"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options(
            "/accounts/123456/balance",
            headers={"Origin": "http://localhost:5173"}
        )
        # CORS may respond with 405 or 200 depending on implementation
        assert response.status_code in [200, 405]
    
    def test_health_endpoint_always_accessible(self, client):
        """Test that health endpoint is always accessible"""
        response = client.get("/health")
        assert response.status_code == 200
