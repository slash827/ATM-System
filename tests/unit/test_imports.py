#!/usr/bin/env python3
"""Test script for backend imports"""

import sys
import traceback

def test_import():
    try:
        print("Testing backend imports...")
        
        # Test step by step
        print("1. Importing backend.core.config...")
        from backend.core.config import settings
        print(f"   ✅ Settings: {settings.app_name}")
        
        print("2. Importing backend.core.exceptions...")
        from backend.core.exceptions import AccountNotFoundError
        print("   ✅ Exceptions imported")
        
        print("3. Importing backend.api.accounts...")
        from backend.api import accounts
        print("   ✅ Accounts API imported")
        
        print("4. Importing main app...")
        from backend.main import app
        print("   ✅ Main app imported successfully!")
        
        print(f"5. App type: {type(app)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)
