"""
Authentication APIs
"""

from fastapi import APIRouter, Body
from fastapi.responses import ORJSONResponse

from errorhub.decorator import api_exception_handler

from models.auth import LoginRequestModel, LoginResponse, LogoutRequestModel
from models.users import UserResponse

from logic.factory import factory

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
    auth_service = factory.get_authentication_service()

    result = await auth_service.login(
        credentials={
            "email": user_credentials.data.credentials["email"],
            "password": user_credentials.data.credentials["password"],
        },
        strategy_name=user_credentials.data.strategy,
    )

    user = result["user"]

    response = LoginResponse(
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            apps=user.apps,
        ),
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
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
    auth_service = factory.get_authentication_service()

    await auth_service.logout(
        refresh_token=logout_request.data.refresh_token,
    )

    return {"message": "User logged out successfully"}
