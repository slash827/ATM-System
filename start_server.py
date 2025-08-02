#!/usr/bin/env python3
"""
Railway startup script for ATM System
Handles port detection and starts the server
"""
import os
import subprocess
import sys

def main():
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
    
    print(f"Starting ATM System server on port {port_num}...")
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
