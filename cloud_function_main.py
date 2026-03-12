"""Cloud Functions entry point for Löneprocess API

This file wraps the FastAPI app for Firebase Cloud Functions.
DO NOT run this locally - use main.py instead.
"""
import functions_framework
from main import app

@functions_framework.http
def loneprocess_api(request):
    """HTTP Cloud Function entry point
    
    This function is called by Firebase when requests come in.
    It forwards all requests to the FastAPI app.
    """
    # FastAPI's ASGI app can be called directly with the request
    from asgiref.sync import async_to_sync
    from starlette.requests import Request
    from starlette.responses import Response
    
    # Convert Cloud Functions request to ASGI scope
    scope = {
        'type': 'http',
        'asgi': {'version': '3.0'},
        'http_version': '1.1',
        'method': request.method,
        'scheme': 'https',
        'path': request.path,
        'query_string': request.query_string.encode() if request.query_string else b'',
        'headers': [(k.lower().encode(), v.encode()) for k, v in request.headers.items()],
        'server': ('localhost', 443),
    }
    
    # Create ASGI receive and send callables
    async def receive():
        return {
            'type': 'http.request',
            'body': request.get_data(),
        }
    
    response_started = False
    status_code = 200
    response_headers = []
    response_body = []
    
    async def send(message):
        nonlocal response_started, status_code, response_headers, response_body
        
        if message['type'] == 'http.response.start':
            response_started = True
            status_code = message['status']
            response_headers = message.get('headers', [])
        elif message['type'] == 'http.response.body':
            response_body.append(message.get('body', b''))
    
    # Call the FastAPI app
    async_to_sync(app)(scope, receive, send)
    
    # Build response
    headers_dict = {k.decode(): v.decode() for k, v in response_headers}
    body = b''.join(response_body)
    
    return (body, status_code, headers_dict)
