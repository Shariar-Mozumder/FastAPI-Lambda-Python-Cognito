from fastapi import APIRouter
from ..services import auth_service

auth_router = APIRouter()

@auth_router.post("/signup/")
async def signup(request: dict):
    response=auth_service.signup(request)
    return response

@auth_router.post("/verification/")
async def verification(request: dict):
    response=auth_service.verification(request)
    return response

@auth_router.post("/signin/")
async def signin(request: dict):
    response=auth_service.signin(request)
    return response