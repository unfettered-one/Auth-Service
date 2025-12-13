"""
Authentication APIs
"""

from fastapi import APIRouter, Body, Security
from fastapi.responses import ORJSONResponse

from errorhub.decorator import api_exception_handler

from auth_service.models.auth import (
    LoginRequestModel,
    LoginResponse,
    LogoutRequestModel,
    TokenRequestModel,
    TokenRefreshResponse,
)
from auth_service.models.users import UserResponse

from auth_service.logic.factory import factory
from auth_service.middleware.auth_dependency import get_current_user

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
        refresh_token=result["refresh_token"],  # TODO remove later and store in http cookie
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
async def logout(logout_request: LogoutRequestModel = Body(...), token_data=Security(get_current_user)):
    """
    User logout endpoint
    """
    auth_service = factory.get_authentication_service()

    await auth_service.logout(
        refresh_token=logout_request.data.refresh_token,
    )

    return {"message": "User logged out successfully"}


@router.post(
    "/auth/refresh",
    summary="Refresh access token",
    responses={200: {"description": "Token refreshed successfully", "model": TokenRefreshResponse}},
    tags=["Authentication"],
)
@api_exception_handler
async def refresh_token(
    refresh_request: TokenRequestModel = Body(...),
):
    """
    Refresh access token and refresh token
    """

    auth_service = factory.get_authentication_service()
    tokens = await auth_service.refresh(refresh_request.data.refresh_token)
    tokens_response = TokenRefreshResponse(**tokens)
    return ORJSONResponse(content=tokens_response.model_dump(), status_code=200)


@router.get(
    "/auth/me",
    summary="Get current user info",
    responses={200: {"description": "Current user info", "model": UserResponse}},
    tags=["Authentication"],
)
@api_exception_handler
async def get_current_user_info(
    payload=Security(get_current_user),
):
    user_id = payload["sub"]

    user_service = factory.get_user_service()
    user = await user_service.get_user_info(user_id, None)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        apps=user.apps,
    )
