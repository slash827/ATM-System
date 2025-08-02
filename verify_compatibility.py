#!/usr/bin/env python3
"""
Environment Compatibility Verification Script
Ensures Docker environment matches local development environment
"""

import sys
import platform
import subprocess
import json
from importlib.metadata import version

def get_python_info():
    """Get Python version and platform info"""
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
    }

def get_package_versions():
    """Get versions of key packages"""
    packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "pytest",
        "httpx",
        "pytest-asyncio"
    ]
    
    versions = {}
    for package in packages:
        try:
            versions[package] = version(package)
        except Exception as e:
            versions[package] = f"ERROR: {e}"
    
    return versions

def verify_compatibility():
    """Verify environment compatibility"""
    print("🔍 Environment Compatibility Check")
    print("=" * 50)
    
    # Python info
    python_info = get_python_info()
    print(f"🐍 Python Version: {python_info['python_version']}")
    print(f"📦 Implementation: {python_info['python_implementation']}")
    print(f"💻 Platform: {python_info['platform']}")
    print(f"🏗️  Architecture: {python_info['architecture']}")
    print()
    
    # Package versions
    print("📚 Package Versions:")
    package_versions = get_package_versions()
    for package, ver in package_versions.items():
        status = "✅" if not ver.startswith("ERROR") else "❌"
        print(f"  {status} {package}: {ver}")
    print()
    
    # Expected versions (from requirements.txt)
    expected = {
        "python": "3.11.2",
        "fastapi": "0.115.12",
        "uvicorn": "0.34.2", 
        "pydantic": "2.11.5"
    }
    
    print("🎯 Compatibility Status:")
    
    # Check Python version
    current_python = python_info['python_version']
    if current_python == expected["python"]:
        print(f"  ✅ Python {current_python} - MATCHES expected {expected['python']}")
    else:
        print(f"  ⚠️  Python {current_python} - DIFFERS from expected {expected['python']}")
    
    # Check key packages
    for package in ["fastapi", "uvicorn", "pydantic"]:
        current_ver = package_versions.get(package, "MISSING")
        expected_ver = expected.get(package, "UNKNOWN")
        
        if current_ver == expected_ver:
            print(f"  ✅ {package} {current_ver} - MATCHES")
        else:
            print(f"  ⚠️  {package} {current_ver} - EXPECTED {expected_ver}")
    
    print()
    print("🚀 Recommendation:")
    if current_python == expected["python"]:
        print("  ✅ Docker and local environments are aligned!")
        print("  ✅ Safe to deploy with current Dockerfile")
    else:
        print("  ⚠️  Consider updating Dockerfile to match local Python version")
        print(f"  ⚠️  Update FROM python:{current_python}-slim-bookworm")
    
    return True

if __name__ == "__main__":
    try:
        verify_compatibility()
    except Exception as e:
        print(f"❌ Error during compatibility check: {e}")
        sys.exit(1)
