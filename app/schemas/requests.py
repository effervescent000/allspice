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
    id: int | None = None
    name: str
    description: str | None = None


class WordLinkRequest(BaseRequest):
    id: int | None = None
    definition: str
    hint: str | None = None
    part_of_speech: str


class WordRequest(BaseRequest):
    id: int | None = None
    word: str
    part_of_speech: str
    notes: str | None = None
    language_id: int

    word_link_ids: list[int] = []


class SCInput(BaseRequest):
    word_list: list[str]
    sound_changes: str
