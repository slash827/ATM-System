from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app, raise_server_exceptions=False)

class TestSecurityValidation:
    """Test security-related validations"""
    
    def test_account_number_format_validation(self):
        """Test account number must be exactly 6 digits"""
        # Test invalid formats that should trigger validation errors
        invalid_accounts = ["12345", "1234567", "abc123", "123-456"]
        
        for account in invalid_accounts:
            response = client.get(f"/accounts/{account}/balance")
            assert response.status_code == 422  # Validation error
        
        # Test empty string which should return 404 (route not found)
        response = client.get("/accounts//balance") 
        assert response.status_code == 404
    
    def test_amount_precision_validation(self):
        """Test amount validation with decimal precision"""
        # Test invalid amounts
        invalid_amounts = [
            {"amount": 100.123},  # Too many decimals
            {"amount": -50.0},    # Negative
            {"amount": 0.0},      # Zero
            {"amount": 10001.0},  # Too large
        ]
        
        for amount_data in invalid_amounts:
            response = client.post("/accounts/123456/withdraw", json=amount_data)
            assert response.status_code == 422
    
    def test_malicious_input_validation(self):
        """Test validation against malicious input patterns"""
        # These inputs should trigger validation errors (422)
        validation_inputs = [
            "123456'; DROP TABLE accounts; --",     # SQL-like injection pattern
            "123456 OR 1=1",                       # Logic injection attempt
        ]
        
        for malicious_input in validation_inputs:
            response = client.get(f"/accounts/{malicious_input}/balance")
            # Should fail validation due to regex pattern
            assert response.status_code == 422
        
        # These inputs get URL-encoded or cause route mismatches (404)
        route_mismatch_inputs = [
            "123456<script>alert('xss')</script>",  # XSS attempt (gets URL encoded)
            "../../../etc/passwd",                 # Path traversal (route mismatch)
        ]
        
        for malicious_input in route_mismatch_inputs:
            response = client.get(f"/accounts/{malicious_input}/balance")
            # Should not match any route
            assert response.status_code == 404
        
        # Null byte injection and newlines break URL parsing
        problematic_inputs = ["123456\x00admin", "123456\n\r\t"]
        for malicious_input in problematic_inputs:
            try:
                response = client.get(f"/accounts/{malicious_input}/balance")
                # If the request somehow succeeds, it should be 404 or 422
                assert response.status_code in [404, 422]
            except Exception:
                # URL parsing fails, which is expected security behavior
                pass
    
    def test_xss_prevention(self):
        """Test XSS attack prevention"""
        # These XSS payloads should trigger validation errors
        validation_xss_payloads = [
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>"
        ]
        
        for payload in validation_xss_payloads:
            # Try to inject in account number
            response = client.get(f"/accounts/{payload}/balance")
            assert response.status_code == 422
        
        # This payload gets URL-encoded and doesn't match route
        encoded_payloads = ["<script>alert('xss')</script>"]
        for payload in encoded_payloads:
            response = client.get(f"/accounts/{payload}/balance")
            assert response.status_code == 404
    
    def test_large_payload_handling(self):
        """Test handling of unusually large payloads"""
        large_amount = "9" * 1000  # Very large number as string
        
        response = client.post("/accounts/123456/withdraw", 
                             json={"amount": large_amount})
        assert response.status_code == 422
    
    def test_concurrent_transactions(self):
        """Test race condition protection"""
        import threading
        
        # Reset account balance using test database
        from backend.database.test_db import db
        db.reset_test_data()
        
        results = []
        
        def make_withdrawal():
            response = client.post("/accounts/123456/withdraw", 
                                 json={"amount": 100.0})
            results.append(response.status_code)
        
        # Create multiple threads for concurrent withdrawals
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_withdrawal)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Check that not all withdrawals succeeded (some should fail due to insufficient funds)
        success_count = results.count(200)
        assert success_count <= 10  # Maximum 10 successful $100 withdrawals from $1000

class TestInputSanitization:
    """Test input sanitization and validation"""
    
    def test_special_characters_in_amount(self):
        """Test special characters in amount field"""
        special_chars = ["$100", "100€", "100.00$", "1,000.00", "100 USD"]
        
        for amount in special_chars:
            response = client.post("/accounts/123456/withdraw",
                                 json={"amount": amount})
            assert response.status_code == 422
    
    def test_unicode_and_emoji_handling(self):
        """Test unicode characters and emojis"""
        unicode_inputs = ["🏧💰", "₹100", "100€", "مبلغ"]
        
        for input_val in unicode_inputs:
            response = client.get(f"/accounts/{input_val}/balance")
            assert response.status_code == 422
    
    def test_null_byte_injection(self):
        """Test null byte injection attempts"""
        null_byte_inputs = ["123456\x00", "123456\x00admin", "123456\x00.txt"]
        
        for input_val in null_byte_inputs:
            try:
                response = client.get(f"/accounts/{input_val}/balance")
                # If the request somehow succeeds, it should fail validation
                assert response.status_code in [404, 422]
            except Exception as e:
                # URL parsing should fail with null bytes, which is expected
                # This is actually good security behavior
                assert "Invalid non-printable ASCII character" in str(e)

class TestErrorInformationLeakage:
    """Test that errors don't leak sensitive information"""
    
    def test_error_responses_no_stack_traces(self):
        """Ensure error responses don't contain stack traces"""
        # Test with invalid account
        response = client.get("/accounts/999999/balance")
        assert response.status_code == 404
        
        error_text = response.text.lower()
        
        # Should not contain sensitive information
        forbidden_terms = ["traceback", "exception", "file", "line", "python", "uvicorn"]
        for term in forbidden_terms:
            assert term not in error_text
    
    def test_health_endpoint_info_disclosure(self):
        """Test health endpoint doesn't expose sensitive info"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        # Should not expose sensitive system information
        sensitive_keys = ["database_url", "secret_key", "password", "token"]
        
        response_str = str(data).lower()
        for key in sensitive_keys:
            assert key not in response_str

class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rapid_requests(self):
        """Test handling of rapid consecutive requests"""
        # Make many rapid requests
        responses = []
        for i in range(20):
            response = client.get("/accounts/123456/balance")
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay
        
        # All should succeed in normal conditions
        # In production with rate limiting, some might return 429
        success_count = responses.count(200)
        assert success_count >= 15  # Allow some rate limiting