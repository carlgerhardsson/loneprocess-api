"""Firebase Cloud Functions entry point

This is the ONLY file Firebase Functions will look for.
It must be named main.py or have functions decorated with @https_fn.on_request
"""
from firebase_functions import https_fn
from firebase_admin import initialize_app
import json

# Initialize Firebase Admin
try:
    initialize_app()
except ValueError:
    pass  # Already initialized

# Import the FastAPI app
from main import app as fastapi_app

@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    """Cloud Function that wraps FastAPI
    
    This function receives HTTP requests from Cloud Functions
    and forwards them to the FastAPI application.
    """
    # Use Mangum to adapt FastAPI ASGI app to Cloud Functions
    from mangum import Mangum
    
    # Create handler
    handler = Mangum(fastapi_app, lifespan="off")
    
    # Convert Cloud Functions request to ASGI event
    event = {
        "requestContext": {"http": {"method": req.method}},
        "headers": dict(req.headers),
        "body": req.get_data(as_text=True) if req.method in ["POST", "PUT", "PATCH"] else None,
        "isBase64Encoded": False,
        "rawPath": req.path,
        "rawQueryString": req.query_string.decode(),
    }
    
    # Call handler
    result = handler(event, {})
    
    # Return response
    return https_fn.Response(
        result.get("body", ""),
        status=result.get("statusCode", 200),
        headers=result.get("headers", {})
    )
