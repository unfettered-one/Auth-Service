from auth_service.models.base import BaseModelForbidExtra
from auth_service.models.users import UserResponse


class LoginModel(BaseModelForbidExtra):
    strategy: str
    credentials: dict


class LoginRequestModel(BaseModelForbidExtra):
    data: LoginModel


class LoginResponse(BaseModelForbidExtra):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes default


class LogoutModel(BaseModelForbidExtra):
    refresh_token: str


class LogoutRequestModel(BaseModelForbidExtra):
    data: LogoutModel


class TokenModel(BaseModelForbidExtra):
    access_token: str
    refresh_token: str


class TokenRequestModel(BaseModelForbidExtra):
    data: TokenModel


class TokenRefreshResponse(BaseModelForbidExtra):
    access_token: str
    refresh_token: str
