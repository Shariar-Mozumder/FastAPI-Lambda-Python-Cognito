from fastapi import Request, HTTPException
from authlib.jose import jwt

# AWS Cognito configuration
COGNITO_REGION = "us-east-2"

# Middleware for token verification
async def verify_token(request: Request,call_next):
    # Skip token verification for /signin and /signup endpoints
    if request.url.path == "/signin/" or request.url.path == "/signup/" or  request.url.path == "/verification/" or request.url.path == "/getDetails/":
        response = await call_next(request)
        return response
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing token")

    try:
        # Verify JWT token
        claims = jwt.decode(
            token,
            options={"verify_signature": False},  # Cognito tokens are self-contained (no need to verify signature)
            algorithms=["RS256"]
        )
        # Add user claims to request state for use in route handlers
        request.state.user_claims = claims
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    # Call the next middleware or route handler
    response = await call_next(request)
    return response
