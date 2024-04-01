from src.utils.response import api_response
from src.models.user_model import User
def get_details(name,role,age):
    try:
        
        payload={
            "Name":name,
            "Role":role,
            "Age": str(age)
        }
        return api_response(200,"get details sucessfully",payload)
    except Exception as e:
        return {"error msg: "+str(e)}
    
def create_user(userData):
    try:
        user_id = userData.get('email')  # Assuming email is unique and can be used as user_id
        full_name = userData.get('full_name')
        email = userData.get('email')
        age = userData.get('age')
        phone = userData.get('phone')
        password=userData.get('password')
        token=userData.get('token')
        user=User(
            user_id=user_id,
            full_name=full_name,
            email=email,
            age=age,
            phone=phone,
            password=password,
            token=token
            )
        user.save()
        return api_response(200,"User created successfully.",user)
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))

def get_user(email):
    try:
        user=User.get(email)
        if user:
            return api_response(200,"User get successfully.",user)
        else:
            return api_response(200,"User not found.")
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))

def get_all_users():
    users = list(User.scan())
    return users

def update_user(userData):
    user_id=userData.get("email")
    try:
        # Fetch the user by user_id
        user = User.get(user_id)
        # Update the specified attributes
        for key, value in userData.items():
            setattr(user, key, value)
        # Save the changes
        user.save()
        return api_response(200,"User updated successfully.",user)
    except User.DoesNotExist:
        return api_response(200,"User does not exist.")
    
def delete_user(email):
    try:
        user = User.get(email)
        user.delete()
        return api_response(200,"User deleted successfully.")
    except User.DoesNotExist:
        return api_response(500,"User does not exist.")

def get_user_by_name(username):
    try:
        condition=None
        if username:
            condition &= User.full_name.contains(username)
        items=User.scan(filter_condition=condition)
        userList=[User(full_name=item.full_name,email=item.email,age=item.age,phone=item.phone) for item in items]
        return api_response(200, "get Users Successfully.",userList)
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))
        