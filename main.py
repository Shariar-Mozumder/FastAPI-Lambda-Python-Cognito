import os
from fastapi import FastAPI,HTTPException
from mangum import Mangum
import uvicorn
# from pydantic import BaseModel
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from fastapi.middleware.cors import CORSMiddleware

# from passlib.context import CryptContext
from middleware import verify_token

from src.views.user_controller import user_router
from src.views.auth_controller import auth_router



# STAGE = os.environ.get('STAGE')
# root_path = '/' if not STAGE else f'/{STAGE}/'

# app = FastAPI(title="FastAPI x AWS Lambda", root_path=root_path)

app = FastAPI(title="FastAPI x AWS Lambda")

# AWS Cognito configuration


# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

origins = [
    "*" # Example: Allow requests from this origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# Add token verification middleware
# app.middleware("http")(verify_token)

# Include routers from different controllers
app.include_router(user_router)
app.include_router(auth_router)



# Mangum Handler, this is so important
handler = Mangum(app)

#  # at last, the bottom of the file/module
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5049)
