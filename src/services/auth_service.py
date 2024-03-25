import boto3
from src.utils.response import api_response

COGNITO_USER_POOL_ID = "us-east-2_L79cAUYQW"
COGNITO_REGION = "us-east-2"

cognito = boto3.client("cognito-idp", region_name=COGNITO_REGION)

# Sign up endpoint
def signup(requestData):
    try:
        request_obj= requestData.get("ObjBody")
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
        return api_response(200, "User signed up successfully")
    except Exception as e:
        return api_response(500, "Server error: "+str(e))
    
def verification(requestData):
    request_obj= requestData.get("ObjBody")
    verification_code = request_obj.get("VerficationCode")
    user_email = request_obj.get("Email")
    try:
        # Confirm the user sign-up
        response = cognito.confirm_sign_up(
            ClientId='1a4ou6taon6on7spbva70tuol0',  # Replace with your Cognito app client ID
            Username=user_email,
            ConfirmationCode=verification_code
        )
        return api_response(200,"User confirmed successfully!")
    except Exception as e:
        return api_response(500,"Server error: "+ str(e))
    
def signin(requestData):
    try:
        request_obj= requestData.get("ObjBody")
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
        return api_response(200,"logged in successfully",{"token": token})
    except Exception as e:
        raise api_response(500, "Server error: "+str(e))