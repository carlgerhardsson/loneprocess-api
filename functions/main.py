"""Firebase Cloud Functions entry point for Löneprocess API"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import from root
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app
from main import app

# For Firebase Functions 2nd gen (Python)
import functions_framework

@functions_framework.http
def loneprocess_api(request):
    """HTTP Cloud Function entry point"""
    return app(request)
