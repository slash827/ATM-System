#!/bin/bash
# Simple startup script for Railway
echo "Starting ATM System on port $PORT"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
