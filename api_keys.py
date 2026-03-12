"""
API Key Management
Centralized storage and validation of API keys
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# API Keys Registry
# Format: {"key": "description/team_name"}
API_KEYS: Dict[str, str] = {
    # Frontend Team X
    "wXWoaJ13LTuPVcxqmzLYFKz9euJw_h4V7PkWnEfvONs": "Frontend Team X",
    
    # Internal Development
    "zXb_f7MYOeXdnPe6iQPc7VrD1pMH5AC388AM1YfFdyc": "Internal Dev Team",
    
    # Testing/QA
    "BptF6lJZqhynSameW-OiNtLodKt3tsi0IPSukpV8nxA": "Testing/QA",
}

def validate_api_key(api_key: str) -> Optional[str]:
    """
    Validate an API key and return the team name if valid.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Team name if valid, None if invalid
    """
    team_name = API_KEYS.get(api_key)
    
    if team_name:
        logger.info(f"✅ Valid API key for: {team_name}")
    else:
        logger.warning(f"❌ Invalid API key attempted: {api_key[:10]}...")
    
    return team_name

def get_all_teams() -> list:
    """Get list of all registered teams"""
    return list(API_KEYS.values())

def revoke_key(api_key: str) -> bool:
    """
    Revoke an API key.
    
    Args:
        api_key: The key to revoke
        
    Returns:
        True if key was revoked, False if key didn't exist
    """
    if api_key in API_KEYS:
        team_name = API_KEYS[api_key]
        del API_KEYS[api_key]
        logger.info(f"🔴 Revoked API key for: {team_name}")
        return True
    return False

# Export
__all__ = ['validate_api_key', 'get_all_teams', 'revoke_key', 'API_KEYS']
