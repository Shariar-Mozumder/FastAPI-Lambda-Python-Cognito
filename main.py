import os
from fastapi import FastAPI,Request,HTTPException, Depends
from mangum import Mangum
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import boto3
from passlib.context import CryptContext
from middleware import verify_token

# STAGE = os.environ.get('STAGE')
# root_path = '/' if not STAGE else f'/{STAGE}/'

# app = FastAPI(title="FastAPI x AWS Lambda", root_path=root_path)

app = FastAPI(title="FastAPI x AWS Lambda")

# AWS Cognito configuration
COGNITO_USER_POOL_ID = "us-east-2_L79cAUYQW"
COGNITO_REGION = "us-east-2"

# cognito = boto3.client("cognito-idp", region_name=COGNITO_REGION)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

class RequestBody(BaseModel):
   ObjBody: dict
   ListBody: list


# Sign up endpoint
@app.post("/signup/")
async def signup(request: RequestBody):
    try:
        request_obj= request.ObjBody
        full_name = request_obj.get("FullName")
        phone = request_obj.get("Phone")
        user_id = request_obj.get("UserID")
        email = request_obj.get("Email")
        password = request_obj.get("Password")


        # Create user in Cognito User Pool
        response = cognito.sign_up(
            ClientId="1a4ou6taon6on7spbva70tuol0",  # Replace with your Cognito app client ID
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "custom:name", "Value": full_name},
                {"Name": "custom:phone_number", "Value": phone},
                {"Name": "custom:userId", "Value": user_id},
                {"Name": "email", "Value": email}
            ]
        )
        return {"message": "User signed up successfully"}
    except cognito.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#verification Email
@app.post("/verification/")
async def verification(request: RequestBody):
    request_obj= request.ObjBody
    verification_code = request_obj.get("VerficationCode")
    user_email = request_obj.get("Email")
    try:
        # Confirm the user sign-up
        response = cognito.confirm_sign_up(
            ClientId='1a4ou6taon6on7spbva70tuol0',  # Replace with your Cognito app client ID
            Username=user_email,
            ConfirmationCode=verification_code
        )
        print("User confirmed successfully!")
    except cognito.exceptions.UserNotFoundException:
        print("User not found.")
    except cognito.exceptions.CodeMismatchException:
        print("Verification code does not match.")
    except cognito.exceptions.ExpiredCodeException:
        print("Verification code has expired.")
    except Exception as e:
        print("An error occurred:", str(e))

# Sign in endpoint
@app.post("/signin/")
async def signin(request: RequestBody):
    try:
        request_obj= request.ObjBody
        email = request_obj.get("Email")
        password = request_obj.get("Password")
        # Authenticate user with Cognito
        response = cognito.initiate_auth(
            ClientId="1a4ou6taon6on7spbva70tuol0",  # Replace with your Cognito app client ID
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password}
        )

        # Generate JWT token
        token = response["AuthenticationResult"]["AccessToken"]
        return {"token": token}
    except cognito.exceptions.UserNotFoundException:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    except cognito.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get('hello/')
def hello_api(name: str = 'World'):
    return {"hello": name}

# @app.post("/")
# def hello_world(request: RequestBody):
#     try:
#         request_obj= request.ObjBody
#         name = request_obj.get("Name")
#         role = request_obj.get("Role")
#         age = request_obj.get("Age")
#         return{
#             "Your Name: "+name,
#             "Your Role: "+role,
#             "Your Age: "+str(age)
#         }
#     except Exception as e:
#         return {"error msg: "+str(e)}

@app.post("/getDetails/")
def process_request(request: RequestBody):
    # request_body = await request.json()
    try:
        request_obj= request.ObjBody
        name = request_obj.get("Name")
        role = request_obj.get("Role")
        age = request_obj.get("Age")
        return{
            "Name":name,
            "Role":role,
            "Age": str(age)
        }
    except Exception as e:
        return {"error msg: "+str(e)}



# Mangum Handler, this is so important
handler = Mangum(app)

#  # at last, the bottom of the file/module
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5049)
