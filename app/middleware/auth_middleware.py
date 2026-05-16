from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from ..auth.jwt_handler import verify_token


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for login, docs and websocket
        path = request.url.path
        if path.startswith("/auth") or path.startswith("/openapi.json") or path.startswith("/docs") or path.startswith("/ws"):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth:
            return JSONResponse({"success": False, "message": "Missing authorization"}, status_code=401)
        try:
            token = auth.split(" ")[1]
            verify_token(token)
        except Exception:
            return JSONResponse({"success": False, "message": "Invalid token"}, status_code=401)

        return await call_next(request)
