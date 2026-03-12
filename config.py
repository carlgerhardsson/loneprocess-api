"""
Firebase configuration for staging environment
Lazy initialization - Firebase is initialized on first use, not at import time
"""
import os
import logging
from firebase_admin import credentials, firestore, initialize_app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
_db = None
_initialized = False

def get_firebase_credentials_path():
    """Get Firebase credentials path - supports both local and Cloud Run."""
    # Cloud Run: Uses Application Default Credentials automatically
    # Local: Uses credentials file
    
    creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_json:
        logger.info(f"Using GOOGLE_APPLICATION_CREDENTIALS: {creds_json}")
        return creds_json
    
    # Local development path
    local_path = os.path.join('credentials', 'loneprocess-api-staging-firebase-adminsdk-fbsvc-f174b6cb01.json')
    if os.path.exists(local_path):
        logger.info(f"Using local credentials: {local_path}")
        return local_path
    
    # Cloud Run - no explicit credentials needed
    logger.info("Using Application Default Credentials (Cloud Run)")
    return None

def initialize_firebase():
    """Initialize Firebase (called on first use)"""
    global _initialized
    
    if _initialized:
        logger.info("Firebase already initialized")
        return
    
    try:
        creds_path = get_firebase_credentials_path()
        
        if creds_path:
            cred = credentials.Certificate(creds_path)
            initialize_app(cred)
            logger.info("✅ Firebase initialized with credentials file")
        else:
            # Cloud Run uses ADC
            initialize_app()
            logger.info("✅ Firebase initialized with Application Default Credentials")
        
        _initialized = True
        logger.info("✅ Firebase initialization complete")
        
    except Exception as e:
        logger.error(f"❌ Firebase initialization failed: {e}")
        raise

def get_db():
    """Get Firestore client (lazy initialization)"""
    global _db
    
    if _db is None:
        if not _initialized:
            initialize_firebase()
        _db = firestore.client()
        logger.info("✅ Firestore client created")
    
    return _db

# For backward compatibility - but this will trigger lazy init
@property
def db():
    """Firestore database client (lazy initialized)"""
    return get_db()

# Export for use in other modules
__all__ = ['get_db', 'initialize_firebase']
