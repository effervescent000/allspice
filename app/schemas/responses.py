from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: str
    username: str


class LanguageResponse(BaseResponse):
    id: int
    name: str
    description: str | None


class WordLinkResponse(BaseResponse):
    id: int
    definition: str
    hint: str | None
    part_of_speech: str


class WordResponse(BaseResponse):
    id: int
    word: str
    part_of_speech: str
    notes: str | None

    word_links: list[WordLinkResponse]

    language_id: int


class PhoneResponse(BaseResponse):
    id: int
    base_phone: str
    quality: str | None
    graph: str | None
    vowel: bool
    language_id: int

    composed_phone: str


class SCOutput(BaseResponse):
    output: list[str]


class SoundChangeRulesResponse(BaseResponse):
    id: int
    name: str | None
    content: str
    role: str | None
    language_id: int


class WordClassResponse(BaseResponse):
    id: int
    name: str
    abbreviation: str
    part_of_speech: str
    language_id: int
