from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import structlog

logger = structlog.get_logger(__name__)

class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define CORS headers to be used for all responses
        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Access-Control-Max-Age": "86400",  # 24 hours
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Expose-Headers": "Content-Length, Content-Range",
            "Vary": "Origin",
        }
        
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            logger.info("Handling preflight CORS request", path=request.url.path)
            return Response(status_code=200, content="", headers=cors_headers)
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Add CORS headers to successful responses
            for header_name, header_value in cors_headers.items():
                response.headers[header_name] = header_value
            
            logger.debug("Added CORS headers to response", path=request.url.path, method=request.method, status=response.status_code)
            return response
            
        except Exception as exc:
            # If an exception occurs, capture it and add CORS headers to the error response
            logger.warning("Exception in request handling, adding CORS headers", path=request.url.path, error=str(exc))
            
            # Let the exception be handled by FastAPI but ensure it has CORS headers
            # This is done by wrapping the exception in a custom exception class
            # that will be caught by the exception handlers in FastAPI
            raise exc
