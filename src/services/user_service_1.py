from src.utils.response import api_response
from src.models.user_model_1 import Entity,User
from datetime import datetime
from src.utils import utilities
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
        emai_id = userData.get('email')  # Assuming email is unique and can be used as user_id
        name = userData.get('name')
        email = userData.get('email')
        description = userData.get('description')
        phone = userData.get('phone')
        im=userData.get('im')
        modified_by=userData.get('name')
        first_name= userData.get('first_name')
        last_name=userData.get('last_name')
        cell_phone=userData.get('phone')
        user=User(
            id=emai_id,
            name=name,
            email=email,
            description=description,
            phone=phone,
            im=im,
            modified_by=modified_by,
            modified_date=datetime.now(),
            registration_date=datetime.now(),
            status="active",
            first_name=first_name,
            last_name=last_name,
            cell_phone=cell_phone
            )
        user.save()
        return api_response(200,"User created successfully.",utilities.object_to_dict(user))
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))

def get_user(email):
    try:
        user=User.get(email)
        if user:
            return api_response(200,"User get successfully.",utilities.object_to_dict(user))
        else:
            return api_response(200,"User not found.")
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))

def get_all_users():
    try:
        users = list(User.scan())
        if len(users)>0:
            userlist=[]
            for user in users:
                singleUser=utilities.object_to_dict(user)
                userlist.append(singleUser)
            return api_response(200,"User get successfully.",userlist)
        else:
            return api_response(200,"User not found.")
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))

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
        return api_response(200,"User updated successfully.",utilities.object_to_dict(user))
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
            condition &= User.first_name.contains(username)
        items=User.scan(filter_condition=condition)
        # userList=[User(full_name=item.full_name,email=item.email,age=item.age,phone=item.phone) for item in items]
        itemlist=[]
        for item in items:
            singleItem=utilities.object_to_dict(item)
            itemlist.append(singleItem)
        return api_response(200, "get Users Successfully.",itemlist)
    except Exception as e:
        return api_response(500,"Server Error: "+str(e))
        