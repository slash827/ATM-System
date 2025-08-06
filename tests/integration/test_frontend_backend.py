#!/usr/bin/env python3
"""
Frontend-Backend Integration Test Script
Tests all ATM operations that the frontend would use
"""

import requests

BASE_URL = "http://localhost:8000"
FRONTEND_ORIGIN = "http://localhost:5173"

def test_cors_preflight():
    """Test CORS preflight request"""
    print("🔍 Testing CORS preflight...")
    response = requests.options(
        f"{BASE_URL}/accounts/123456/balance",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type"
        }
    )
    print(f"   Preflight Status: {response.status_code}")
    print(f"   CORS Headers: {dict(response.headers)}")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    print("   ✅ CORS preflight working!")

def test_balance_check():
    """Test checking account balance"""
    print("\n💰 Testing balance check...")
    response = requests.get(
        f"{BASE_URL}/accounts/123456/balance",
        headers={"Origin": FRONTEND_ORIGIN}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Balance: ${data['balance']}")
    assert response.status_code == 200
    assert "balance" in data
    print("   ✅ Balance check working!")
    return data['balance']

def test_deposit():
    """Test depositing money"""
    print("\n📥 Testing deposit...")
    initial_balance = test_balance_check()
    
    response = requests.post(
        f"{BASE_URL}/accounts/123456/deposit",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Content-Type": "application/json"
        },
        json={"amount": 25.50}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Message: {data.get('message', 'No message')}")
    print(f"   Previous Balance: ${data.get('previous_balance', 'N/A')}")
    print(f"   New Balance: ${data.get('new_balance', 'N/A')}")
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['new_balance'] == initial_balance + 25.50
    print("   ✅ Deposit working!")
    
    return data['new_balance']

def test_withdrawal():
    """Test withdrawing money"""
    print("\n📤 Testing withdrawal...")
    initial_balance = test_balance_check()
    
    response = requests.post(
        f"{BASE_URL}/accounts/123456/withdraw",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Content-Type": "application/json"
        },
        json={"amount": 75.25}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Message: {data.get('message', 'No message')}")
    print(f"   Previous Balance: ${data.get('previous_balance', 'N/A')}")
    print(f"   New Balance: ${data.get('new_balance', 'N/A')}")
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['new_balance'] == initial_balance - 75.25
    print("   ✅ Withdrawal working!")
    
    return data['new_balance']

def test_money_transfer():
    """Test money transfer between accounts"""
    print("\n💸 Testing money transfer...")
    initial_balance = test_balance_check()
    
    response = requests.post(
        f"{BASE_URL}/accounts/123456/transfer",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Content-Type": "application/json"
        },
        json={
            "amount": 50.00,
            "recipient_account": "789012",
            "message": "Test transfer from integration test"
        }
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Message: {data.get('message', 'No message')}")
    print(f"   Transfer ID: {data.get('transfer_id', 'N/A')}")
    print(f"   Sender New Balance: ${data.get('sender_new_balance', 'N/A')}")
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['sender_new_balance'] == initial_balance - 50.00
    print("   ✅ Money transfer working!")

def test_time_deposit():
    """Test creating time deposit"""
    print("\n⏰ Testing time deposit...")
    initial_balance = test_balance_check()
    
    response = requests.post(
        f"{BASE_URL}/accounts/123456/time-deposits",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Content-Type": "application/json"
        },
        json={
            "amount": 100.00,
            "duration_months": 12
        }
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Message: {data.get('message', 'No message')}")
    print(f"   Deposit ID: {data.get('deposit_id', 'N/A')}")
    print(f"   Interest Rate: {data.get('interest_rate', 'N/A')}%")
    print(f"   Account New Balance: ${data.get('account_new_balance', 'N/A')}")
    
    assert response.status_code == 200
    assert data['success'] == True
    print("   ✅ Time deposit working!")

def test_health_check():
    """Test health endpoint"""
    print("\n🏥 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Environment: {data.get('environment', 'N/A')}")
    print(f"   Debug Mode: {data.get('debug', 'N/A')}")
    assert response.status_code == 200
    print("   ✅ Health check working!")

def main():
    """Run all integration tests"""
    print("🚀 Starting Frontend-Backend Integration Tests")
    print("=" * 50)
    
    try:
        test_cors_preflight()
        test_health_check()
        test_balance_check()
        test_deposit()
        test_withdrawal()
        test_money_transfer()
        test_time_deposit()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! Frontend-Backend communication is working!")
        print("✅ CORS is properly configured")
        print("✅ All ATM operations are functional")
        print("✅ Your frontend should work without network errors!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Check the backend server and ensure DEBUG=true is set")

if __name__ == "__main__":
    main()
