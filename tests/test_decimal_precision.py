import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from main import app
from database import db

client = TestClient(app)

class TestDecimalPrecision:
    """Test decimal precision handling in financial transactions"""
    
    def test_high_precision_amounts_rejected(self):
        """Test that amounts with >2 decimal places are rejected"""
        high_precision_amounts = [
            100.123,    # 3 decimal places
            50.1234,    # 4 decimal places  
            25.12345,   # 5 decimal places
            1.001,      # 3 decimal places (small amount)
            999.999,    # 3 decimal places (large amount)
            0.001,      # 3 decimal places (very small)
        ]
        
        for amount in high_precision_amounts:
            # Test withdrawal
            response = client.post("/accounts/123456/withdraw", 
                                 json={"amount": amount})
            assert response.status_code == 422, f"Amount {amount} should be rejected"
            
            # Test deposit  
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            assert response.status_code == 422, f"Amount {amount} should be rejected"
    
    def test_valid_precision_amounts_accepted(self):
        """Test that amounts with ≤2 decimal places are accepted"""
        valid_amounts = [
            100.00,     # Exactly 2 decimal places
            100.12,     # Exactly 2 decimal places
            100.1,      # 1 decimal place
            100,        # Integer (0 decimal places)
            50.5,       # 1 decimal place
            25.25,      # 2 decimal places
        ]
        
        for amount in valid_amounts:
            # Reset account balance
            db.accounts["123456"].balance = Decimal('1000.0')
            
            # Test deposit (should always work)
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            assert response.status_code == 200, f"Amount {amount} should be accepted"
            
            # Test withdrawal (should work if sufficient funds)
            if amount <= 1000:
                response = client.post("/accounts/123456/withdraw",
                                     json={"amount": amount})
                assert response.status_code == 200, f"Amount {amount} should be accepted"
    
    def test_edge_case_amounts(self):
        """Test edge cases for decimal precision"""
        edge_cases = [
            (0.01, 200),    # Minimum practical amount - should work
            (0.10, 200),    # One decimal place - should work  
            (0.001, 422),   # Too many decimals - should fail
            (0.009, 422),   # Too many decimals - should fail
            (100.00, 200),  # Exact 2 decimals - should work
            (100.50, 200),  # Exact 2 decimals - should work
        ]
        
        for amount, expected_status in edge_cases:
            # Reset account balance
            db.accounts["123456"].balance = Decimal('1000.0')
            
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            assert response.status_code == expected_status, \
                f"Amount {amount} should return status {expected_status}"
    
    def test_floating_point_precision_issues(self):
        """Test handling of floating point precision issues"""
        # These might cause floating point precision issues
        problematic_amounts = [
            0.1 + 0.2,      # Equals 0.30000000000000004 in Python
            1.0 / 3.0,      # Equals 0.3333333333333333
            0.1 * 3,        # Equals 0.30000000000000004
        ]
        
        for amount in problematic_amounts:
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            # These should be rejected due to precision issues
            assert response.status_code == 422

class TestFinancialSecurityScenarios:
    """Test financial security scenarios"""
    
    def test_micro_fraction_attack(self):
        """Test protection against micro-fraction attacks"""
        # Scenario: Attacker tries to steal tiny amounts many times
        micro_amounts = [
            0.001,      # $0.001
            0.0001,     # $0.0001  
            0.00001,    # $0.00001
        ]
        
        for amount in micro_amounts:
            response = client.post("/accounts/123456/withdraw",
                                 json={"amount": amount})
            assert response.status_code == 422, \
                f"Micro amount {amount} should be rejected"
    
    def test_rounding_consistency(self):
        """Test that rounding is consistent and secure"""
        # Reset account to known state
        db.accounts["123456"].balance = Decimal('1000.00')
        
        # Deposit exact amount
        response = client.post("/accounts/123456/deposit",
                             json={"amount": 100.12})
        assert response.status_code == 200
        
        # Check balance is exactly what we expect
        response = client.get("/accounts/123456/balance")
        assert response.status_code == 200
        balance = response.json()["balance"]
        assert float(balance) == 1100.12, f"Expected 1100.12, got {balance}"
        
        # Withdraw exact amount
        response = client.post("/accounts/123456/withdraw",
                             json={"amount": 100.12})
        assert response.status_code == 200
        
        # Check balance is back to original
        response = client.get("/accounts/123456/balance")
        assert response.status_code == 200
        balance = response.json()["balance"]
        assert float(balance) == 1000.00, f"Expected 1000.00, got {balance}"
    
    def test_salami_slicing_prevention(self):
        """Test prevention of salami slicing attacks"""
        # Salami slicing: stealing tiny amounts from many transactions
        
        # Try to make many micro-transactions
        for i in range(10):
            response = client.post("/accounts/123456/withdraw",
                                 json={"amount": 0.001})  # $0.001
            assert response.status_code == 422, \
                f"Micro transaction {i+1} should be rejected"
        
        # Verify balance unchanged
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        # Balance should be unchanged since all micro-transactions were rejected
        assert float(balance) == 1000.00

class TestAmountValidationEdgeCases:
    """Test edge cases in amount validation"""
    
    def test_zero_and_negative_amounts(self):
        """Test that zero and negative amounts are rejected"""
        invalid_amounts = [0, 0.0, 0.00, -1, -0.01, -100.50]
        
        for amount in invalid_amounts:
            response = client.post("/accounts/123456/withdraw",
                                 json={"amount": amount})
            assert response.status_code == 422, \
                f"Amount {amount} should be rejected"
            
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            assert response.status_code == 422, \
                f"Amount {amount} should be rejected"
    
    def test_very_large_amounts(self):
        """Test handling of very large amounts"""
        large_amounts = [
            10001,      # Above limit
            100000,     # Way above limit
            999999.99,  # Very large
        ]
        
        for amount in large_amounts:
            response = client.post("/accounts/123456/deposit",
                                 json={"amount": amount})
            assert response.status_code == 422, \
                f"Large amount {amount} should be rejected"
    
    def test_string_amounts_with_decimals(self):
        """Test string amounts that might slip through"""
        string_amounts = [
            "100.123",
            "50.1234", 
            "0.001",
            "999.999"
        ]
        
        for amount in string_amounts:
            response = client.post("/accounts/123456/withdraw",
                                 json={"amount": amount})
            # These should be rejected by Pydantic validation
            assert response.status_code == 422, \
                f"String amount {amount} should be rejected"

class TestFinancialArithmetic:
    """Test that financial arithmetic is precise"""
    
    def setup_method(self):
        """Reset account before each test"""
        db.accounts["123456"].balance = Decimal('1000.00')
    
    def test_precise_addition(self):
        """Test that deposits add precisely"""
        # Deposit 0.01
        response = client.post("/accounts/123456/deposit", json={"amount": 0.01})
        assert response.status_code == 200
        
        # Check balance
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        assert float(balance) == 1000.01
        
        # Deposit 0.99
        response = client.post("/accounts/123456/deposit", json={"amount": 0.99})
        assert response.status_code == 200
        
        # Check balance is exactly 1001.00
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        assert float(balance) == 1001.00
    
    def test_precise_subtraction(self):
        """Test that withdrawals subtract precisely"""
        # Withdraw 0.01
        response = client.post("/accounts/123456/withdraw", json={"amount": 0.01})
        assert response.status_code == 200
        
        # Check balance
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        assert float(balance) == 999.99
        
        # Withdraw 0.99
        response = client.post("/accounts/123456/withdraw", json={"amount": 0.99})
        assert response.status_code == 200
        
        # Check balance is exactly 999.00
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        assert float(balance) == 999.00
    
    def test_no_floating_point_drift(self):
        """Test that repeated operations don't cause floating point drift"""
        initial_balance = 1000.00
        
        # Perform 100 small operations
        for i in range(50):
            # Deposit 0.01
            response = client.post("/accounts/123456/deposit", json={"amount": 0.01})
            assert response.status_code == 200
            
            # Withdraw 0.01
            response = client.post("/accounts/123456/withdraw", json={"amount": 0.01})
            assert response.status_code == 200
        
        # Balance should still be exactly the same
        response = client.get("/accounts/123456/balance")
        balance = response.json()["balance"]
        assert float(balance) == initial_balance, \
            f"Expected {initial_balance}, got {balance} - floating point drift detected!"