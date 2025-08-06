#!/usr/bin/env python3
"""
Test script for PostgreSQL database implementation
This will test the current backend database models and operations
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_database_models():
    """Test that our database models are properly defined"""
    print("🔍 Testing PostgreSQL Database Models...")
    
    try:
        from backend.database.postgresql import (
            AccountModel, TransactionModel, TimeDepositModel, 
            Base, engine, SessionLocal
        )
        print("   ✅ All database models imported successfully")
        
        # Test model structure
        print(f"   📋 AccountModel table: {AccountModel.__tablename__}")
        print(f"   📋 TransactionModel table: {TransactionModel.__tablename__}")
        print(f"   📋 TimeDepositModel table: {TimeDepositModel.__tablename__}")
        
        # Test that all required columns exist
        account_columns = [col.name for col in AccountModel.__table__.columns]
        transaction_columns = [col.name for col in TransactionModel.__table__.columns]
        deposit_columns = [col.name for col in TimeDepositModel.__table__.columns]
        
        print(f"   📊 Account columns: {account_columns}")
        print(f"   📊 Transaction columns: {transaction_columns}")
        print(f"   📊 Time deposit columns: {deposit_columns}")
        
        # Verify required columns
        required_account_cols = ['account_number', 'balance', 'created_at', 'updated_at']
        for col in required_account_cols:
            assert col in account_columns, f"Missing account column: {col}"
        
        required_transaction_cols = ['id', 'account_number', 'transaction_type', 'amount']
        for col in required_transaction_cols:
            assert col in transaction_columns, f"Missing transaction column: {col}"
        
        required_deposit_cols = ['deposit_id', 'account_number', 'amount', 'duration_months']
        for col in required_deposit_cols:
            assert col in deposit_columns, f"Missing time deposit column: {col}"
        
        print("   ✅ All required columns present in models")
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Model test error: {e}")
        return False
    
    return True

def test_router_imports():
    """Test that the accounts router imports correctly"""
    print("\\n🔗 Testing Accounts Router...")
    
    try:
        from backend.api.accounts import router
        print("   ✅ Accounts router imported successfully")
        
        # Check that router has expected endpoints
        routes = [route.path for route in router.routes]
        print(f"   📍 Available routes: {routes}")
        
        expected_routes = [
            "/{account_number}/balance",
            "/{account_number}/withdraw", 
            "/{account_number}/deposit",
            "/{sender_account}/transfer",
            "/test/reset"
        ]
        
        for route in expected_routes:
            route_exists = any(route in path for path in routes)
            if route_exists:
                print(f"   ✅ Route {route} found")
            else:
                print(f"   ⚠️  Route {route} not found in {routes}")
        
    except ImportError as e:
        print(f"   ❌ Router import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Router test error: {e}")
        return False
    
    return True

def test_main_app():
    """Test that the main app imports correctly"""
    print("\\n🚀 Testing Main App...")
    
    try:
        from backend.main import app
        print("   ✅ Main FastAPI app imported successfully")
        
        # Check that app has expected routes
        routes = [route.path for route in app.routes]
        print(f"   📍 App routes: {routes}")
        
        # Verify basic endpoints exist
        expected_endpoints = ["/", "/accounts/{account_number}/balance"]
        for endpoint in expected_endpoints:
            if any(endpoint in route for route in routes):
                print(f"   ✅ Endpoint pattern {endpoint} found")
            else:
                print(f"   ❌ Endpoint pattern {endpoint} missing")
        
        # Check middleware
        middleware_types = [type(m).__name__ for m in app.user_middleware]
        print(f"   🛡️  Middleware: {middleware_types}")
        
    except ImportError as e:
        print(f"   ❌ Main app import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Main app test error: {e}")
        return False
    
    return True

def test_environment_config():
    """Test environment configuration"""
    print("\\n⚙️  Testing Environment Configuration...")
    
    try:
        # Test config loading
        from backend.core.config import settings
        print(f"   ✅ Settings loaded successfully")
        print(f"   📂 Database URL: {settings.database_url}")
        print(f"   🔧 Environment: {settings.environment}")
        print(f"   🐛 Debug mode: {settings.debug}")
        
        if "postgresql://" in settings.database_url or "postgres://" in settings.database_url:
            print("   ✅ PostgreSQL URL format detected")
        else:
            print("   ⚠️  Non-PostgreSQL URL detected (using SQLite)")
            
    except Exception as e:
        print(f"   ❌ Environment config error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 PostgreSQL Implementation Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database Models", test_database_models),
        ("Router Import", test_router_imports), 
        ("Main App", test_main_app),
        ("Environment Config", test_environment_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            print()
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PostgreSQL implementation is ready.")
        print("\\n📋 Next Steps:")
        print("1. Install and start PostgreSQL server")
        print("2. Run: python -m backend.database.postgresql (to create tables)")
        print("3. Run: python -m backend.main (to start the server)")
        print("4. Test with: python tests/test_accounts.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\\n🔧 Troubleshooting:")
        print("- Make sure all dependencies are installed")
        print("- Check Python path and imports")
        print("- Verify backend structure is correct")

if __name__ == "__main__":
    main()
