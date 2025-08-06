#!/usr/bin/env python3
"""
Railway startup script for ATM System
Handles port detection and Python path setup
"""
import os
import subprocess
import sys
from pathlib import Path

def main():
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Set PYTHONPATH environment variable for subprocess
    python_path = os.environ.get('PYTHONPATH', '')
    if python_path:
        python_path = f"{current_dir}:{python_path}"
    else:
        python_path = str(current_dir)
    
    # Get port from environment variable, default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Ensure port is a valid number
    try:
        port_num = int(port)
    except ValueError:
        print(f"Invalid PORT value: {port}, using default 8000")
        port_num = 8000
    
    # Start the server with uvicorn
    cmd = [
        sys.executable, '-m', 'uvicorn', 
        'main:app', 
        '--host', '0.0.0.0', 
        '--port', str(port_num)
    ]
    
    # Set environment for subprocess
    env = os.environ.copy()
    env['PYTHONPATH'] = python_path
    
    print(f"Starting ATM System server on port {port_num}...")
    print(f"PYTHONPATH: {python_path}")
    subprocess.run(cmd, env=env)

if __name__ == '__main__':
    main()
