from fastapi import APIRouter
from ..services import user_service,user_service_1

user_router = APIRouter()

@user_router.post("/getDetails/")
def process_request(request: dict):
    # request_body = await request.json()
    request_obj= request.get("ObjBody")
    name = request_obj.get("Name")
    role = request_obj.get("Role")
    age = request_obj.get("Age")
    res=user_service.get_details(name,role,age)
    return res


@user_router.post("/createUser/")
def createUser(request: dict):
    request_obj= request.get("ObjBody")
    res=user_service_1.create_user(request_obj)
    return res

@user_router.post("/getUser/")
def getUser(request: dict):
    request_obj= request.get("ObjBody")
    res=user_service_1.get_user(request_obj.get("email"))
    return res

@user_router.get("/getAllUser/")
def getUser():
    res=user_service_1.get_all_users()
    return res

@user_router.post("/updateUser/")
def getUser(request: dict):
    request_obj= request.get("ObjBody")
    res=user_service_1.update_user(request_obj)
    return res

@user_router.post("/deleteUser/")
def getUser(request: dict):
    request_obj= request.get("ObjBody")
    res=user_service_1.delete_user(request_obj.get("email"))
    return res

@user_router.post("/getUserByName/")
def getUserByName(request: dict):
    request_obj= request.get("ObjBody")
    res=user_service_1.get_user_by_name(request_obj.get("full_name"))
    return res