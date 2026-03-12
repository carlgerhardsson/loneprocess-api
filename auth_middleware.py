#!/usr/bin/env python3
"""
API Key Authentication Middleware
Validates X-API-Key header on all protected endpoints
"""
from fastapi import Header, HTTPException, status
from typing import Optional
import logging
from api_keys import validate_api_key

logger = logging.getLogger(__name__)

class APIKeyAuth:
    """
    API Key authentication dependency for FastAPI endpoints.
    
    Usage:
        @app.get("/protected", dependencies=[Depends(APIKeyAuth())])
        def protected_endpoint():
            return {"message": "You have access!"}
    """
    
    def __call__(self, x_api_key: Optional[str] = Header(None)):
        """
        Validate the X-API-Key header.
        
        Args:
            x_api_key: API key from X-API-Key header
            
        Raises:
            HTTPException: 401 if key is missing or invalid
            
        Returns:
            Team name if valid
        """
        if not x_api_key:
            logger.warning("❌ Missing X-API-Key header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing API key. Please provide X-API-Key header.",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        team_name = validate_api_key(x_api_key)
        
        if not team_name:
            logger.warning(f"❌ Invalid API key: {x_api_key[:10]}...")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key. Please contact API administrator for a valid key.",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        logger.info(f"✅ Authenticated request from: {team_name}")
        return team_name

# Create singleton instance
api_key_auth = APIKeyAuth()

# Export
__all__ = ['api_key_auth', 'APIKeyAuth']
