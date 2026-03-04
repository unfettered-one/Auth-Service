from auth_service.models.base import BaseModelForbidExtra
from auth_service.models.users import UserResponse


class LoginModel(BaseModelForbidExtra):
    strategy: str
    credentials: dict


class LoginRequestModel(BaseModelForbidExtra):
    data: LoginModel


class LoginResponse(BaseModelForbidExtra):
    """
    Login response with user info only.
    Tokens are returned as HTTP-only cookies, not in response body.
    """

    user: UserResponse
    message: str = "Login successful"
    token_type: str = "cookie"


class LogoutModel(BaseModelForbidExtra):
    """
    Logout model - refresh token is extracted from cookies, not from body.
    """

    pass


class LogoutRequestModel(BaseModelForbidExtra):
    data: LogoutModel


class TokenModel(BaseModelForbidExtra):
    """
    Token refresh request model - tokens are extracted from cookies, not from body.
    """

    pass


class TokenRequestModel(BaseModelForbidExtra):
    data: TokenModel


class TokenRefreshResponse(BaseModelForbidExtra):
    """
    Token refresh response - tokens are returned as HTTP-only cookies, not in response body.
    """

    message: str = "Token refreshed successfully"
    token_type: str = "cookie"
