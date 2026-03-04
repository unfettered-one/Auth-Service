"""
Authentication APIs
"""

from fastapi import APIRouter, Body, Security, Request
from fastapi.responses import ORJSONResponse

from errorhub.decorator import api_exception_handler
from errorhub.exceptions import BadRequestException
from errorhub.models import ErrorSeverity

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
from auth_service.configuration import settings
from auth_service.cookie.cookie_setup import set_auth_cookies, clear_auth_cookies

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
    User login endpoint.
    Returns user info and sets access/refresh tokens as HTTP-only cookies.
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

    response_body = LoginResponse(
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            apps=user.apps,
        ),
    )

    response = ORJSONResponse(status_code=201, content=response_body.model_dump())
    response = set_auth_cookies(response, result["access_token"], result["refresh_token"])
    return response


@router.post(
    "/auth/logout",
    summary="User logout",
    responses={200: {"description": "Logout successful"}},
    tags=["Authentication"],
)
@api_exception_handler
async def logout(
    request: Request,
    logout_request: LogoutRequestModel = Body(...),
    token_data=Security(get_current_user),
):
    """
    User logout endpoint.
    Extracts refresh token from cookies and clears both access/refresh token cookies.
    """
    auth_service = factory.get_authentication_service()

    # Extract refresh token from cookies
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await auth_service.logout(
            refresh_token=refresh_token,
        )

    response = ORJSONResponse(status_code=200, content={"message": "User logged out successfully"})
    response = clear_auth_cookies(response)
    return response


@router.post(
    "/auth/refresh",
    summary="Refresh access token",
    responses={
        200: {
            "description": "Token refreshed successfully",
            "model": TokenRefreshResponse,
        }
    },
    tags=["Authentication"],
)
@api_exception_handler
async def refresh_token(
    request: Request,
    refresh_request: TokenRequestModel = Body(...),
):
    """
    Refresh access token endpoint.
    Extracts refresh token from cookies, generates new tokens, and sets them as cookies.
    """

    auth_service = factory.get_authentication_service()

    # Extract refresh token from cookies
    refresh_token_value = request.cookies.get("refresh_token")

    if not refresh_token_value:
        raise BadRequestException(
            service="Auth Service",
            message="Refresh token missing",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "Refresh token not found in cookies.",
            },
        )

    tokens = await auth_service.refresh(refresh_token_value)

    tokens_response = TokenRefreshResponse()

    response = ORJSONResponse(content=tokens_response.model_dump(), status_code=200)
    response = set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return response


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
