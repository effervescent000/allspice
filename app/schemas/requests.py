from pydantic import BaseModel


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    username: str
    password: str


class LanguageRequest(BaseRequest):
    name: str
    description: str | None
