from fastapi import Request, HTTPException
import base64
import json

# Middleware for token verification
async def verify_token(request: Request, call_next):
    # Skip token verification for certain endpoints
    skip_verification_endpoints = ["/signin/", "/signup/", "/verification/"]
    if request.url.path in skip_verification_endpoints:
        response = await call_next(request)
        return response

    # Extract token from Authorization header
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing token")

    try:
        # Verify JWT token
        # claims = __import__("jwt").decode(token, COGNITO_PUBLIC_KEY, algorithms=["RS256"], options={"verify_exp": True})
        # Add user claims to request state for use in route handlers
        # request.state.user_claims = claims
        
        header, payload = decode_jwt(token)
    # except __import__("jwt").ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Unauthorized: Token has expired")
    # except __import__("jwt").InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401,detail= str(e))

    # Call the next middleware or route handler
    response = await call_next(request)
    return response

def decode_jwt(token):
    try:
        # Split the token into header, payload, and signature
        header, payload, signature = token.split('.')
        
        # Decode the base64-encoded parts
        decoded_header = base64.urlsafe_b64decode(header + '=' * (4 - len(header) % 4)).decode('utf-8')
        decoded_payload = base64.urlsafe_b64decode(payload + '=' * (4 - len(payload) % 4)).decode('utf-8')
        
        # Parse the JSON data
        header_data = json.loads(decoded_header)
        payload_data = json.loads(decoded_payload)
        
        return header_data, payload_data
    except Exception as e:
        print(f"Error decoding JWT token: {e}")
        return None, None
    


# from fastapi import Request, HTTPException
# from authlib.jose import jwt

# # AWS Cognito configuration
# COGNITO_REGION = "your-aws-region"

# # Middleware for token verification
# async def verify_token(request: Request,call_next):
#     # Skip token verification for /signin and /signup endpoints
#     if request.url.path == "/signin/" or request.url.path == "/signup/" or  request.url.path == "/verification/" or request.url.path == "/getDetails/":
#         response = await call_next(request)
#         return response
#     token = request.headers.get("Authorization", "").split("Bearer ")[-1]
#     if not token:
#         raise HTTPException(status_code=401, detail="Unauthorized: Missing token")

#     try:
#         # Verify JWT token
#         claims = jwt.decode(
#             token,
#             options={"verify_signature": False},  # Cognito tokens are self-contained (no need to verify signature)
#             algorithms=["RS256"]
#         )
#         # Add user claims to request state for use in route handlers
#         request.state.user_claims = claims
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
#     # Call the next middleware or route handler
#     response = await call_next(request)
#     return response

# from fastapi import Request, HTTPException
# import jwt
# # from jwt.exceptions import InvalidTokenError
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization

# # AWS Cognito configuration
# COGNITO_REGION = "your-aws-region"

# Your public key obtained from AWS Cognito
# COGNITO_PUBLIC_KEY = """
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyFhKL3JQfIcJh1uFmvOk
# ...
# -----END PUBLIC KEY-----
# """

# # Middleware for token verification
# async def verify_token(request: Request, call_next):
#     # Skip token verification for specific endpoints
#     if request.url.path in ["/signin/", "/signup/", "/verification/", "/getDetails/"]:
#         return await call_next(request)

#     token = request.headers.get("Authorization", "").split("Bearer ")[-1]
#     if not token:
#         raise HTTPException(status_code=401, detail="Unauthorized: Missing token")

#     try:
#         # Decode and verify JWT token
#         claims = jwt.decode(token, COGNITO_PUBLIC_KEY, algorithms=["RS256"], options={"verify_exp": True})
#         # Add user claims to request state for use in route handlers
#         request.state.user_claims = claims
#     # except InvalidTokenError:
#     #     raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")

#     # Call the next middleware or route handler
#     return await call_next(request)