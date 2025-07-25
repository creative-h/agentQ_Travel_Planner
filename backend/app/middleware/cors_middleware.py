from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import structlog

logger = structlog.get_logger(__name__)

class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            logger.info("Handling preflight CORS request")
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers",
                "Access-Control-Max-Age": "86400",  # 24 hours
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "Content-Length, Content-Range",
                "Vary": "Origin",
            }
            return Response(status_code=200, content="", headers=headers)
        
        # Process the request
        response = await call_next(request)
        
        # Always add CORS headers to every response
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers"
        response.headers["Access-Control-Expose-Headers"] = "Content-Length, Content-Range"
        response.headers["Vary"] = "Origin"
        
        logger.debug("Added CORS headers to response", path=request.url.path, method=request.method)
        return response
