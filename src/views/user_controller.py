from fastapi import APIRouter
from ..services import user_service

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
