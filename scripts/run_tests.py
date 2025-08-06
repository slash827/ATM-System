"""
Automated Test Runner Script
This script runs all tests and provides a comprehensive report
"""
import subprocess
import sys
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return Code: {result.returncode}")
        return result.returncode == 0
    
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Run all automated tests"""
    print("🚀 ATM System - Automated Test Suite")
    print("=" * 80)
    
    # Track test results
    results = []
    
    # 1. Install dependencies
    success = run_command(
        "pip install -r requirements.txt",
        "Installing Dependencies"
    )
    results.append(("Install Dependencies", success))
    
    # 2. Run unit tests
    success = run_command(
        "python -m pytest tests/unit/ -v --tb=short",
        "Running Unit Tests"
    )
    results.append(("Unit Tests", success))
    
    # 3. Run API tests
    success = run_command(
        "python -m pytest tests/api/ -v --tb=short",
        "Running API Integration Tests"
    )
    results.append(("API Tests", success))
    
    # 4. Run all tests with coverage
    success = run_command(
        "python -m pytest tests/ -v --cov=backend --cov-report=term-missing",
        "Running Full Test Suite with Coverage"
    )
    results.append(("Full Test Suite", success))
    
    # 5. Test backend startup
    print(f"\n{'='*60}")
    print("🔥 Testing Backend Startup")
    print(f"{'='*60}")
    
    # Start backend in background
    backend_process = None
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "backend/main.py"],
            cwd=Path(__file__).parent.parent
        )
        
        # Wait for startup
        time.sleep(3)
        
        # Test if it's running
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            backend_success = response.status_code == 200
            print(f"✅ Backend started successfully! Health check: {response.status_code}")
        except Exception as e:
            backend_success = False
            print(f"❌ Backend startup failed: {e}")
        
        results.append(("Backend Startup", backend_success))
        
    finally:
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
    
    # 6. Frontend build test (if Node.js is available)
    success = run_command(
        "cd atm-frontend && npm run build",
        "Testing Frontend Build"
    )
    results.append(("Frontend Build", success))
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\n📈 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
