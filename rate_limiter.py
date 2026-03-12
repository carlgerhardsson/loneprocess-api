"""Rate limiting middleware for FastAPI"""
import time
from collections import defaultdict
from typing import Dict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimiter(BaseHTTPMiddleware):
    """
    Rate limiting middleware
    
    Limits requests to 60 per minute per IP address
    Cost-effective measure to prevent abuse
    """
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Store: {ip: [timestamp1, timestamp2, ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Clean old entries (older than 1 minute)
        current_time = time.time()
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if current_time - timestamp < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            # Return 429 response directly (don't raise exception in middleware)
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per minute allowed",
                    "retry_after": 60,
                    "limit": self.requests_per_minute,
                    "window": "1 minute"
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(current_time + 60)),
                    "Retry-After": "60"
                }
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to successful responses
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers['X-RateLimit-Limit'] = str(self.requests_per_minute)
        response.headers['X-RateLimit-Remaining'] = str(max(0, remaining))
        response.headers['X-RateLimit-Reset'] = str(int(current_time + 60))
        
        return response
