"""
Authentication APIs
"""

from fastapi import APIRouter, Body
from fastapi.responses import ORJSONResponse

from errorhub.decorator import api_exception_handler

from models.auth import LoginRequestModel, LoginResponse, LogoutRequestModel
from models.users import UserResponse


router = APIRouter()


@router.post(
    "/auth/login",
    summary="User login",
    responses={201: {"description": "Login successful", "model": LoginResponse}},
    tags=["Authentication"],
)
@api_exception_handler
async def login(
    user_credentials: LoginRequestModel = Body(...),
):
    """
    User login endpoint
    """
    response = LoginResponse(
        user=UserResponse(id="", name=None, email="123@gmail.com", apps=[]),
        access_token="",
        refresh_token="",
    )
    return ORJSONResponse(
        status_code=201,
        content=response.model_dump(),
    )


@router.post(
    "/auth/logout",
    summary="User logout",
    responses={200: {"description": "Logout successful"}},
    tags=["Authentication"],
)
@api_exception_handler
async def logout(
    logout_request: LogoutRequestModel = Body(...),
):
    """
    User logout endpoint
    """
    return ORJSONResponse(
        status_code=200,
        content={"message": "Logout successful"},
    )
