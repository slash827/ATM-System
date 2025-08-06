import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if now - req_time < self.period
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.calls:
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Try again later."
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        return response