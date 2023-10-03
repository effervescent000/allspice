import json

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core import ValidationError


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


class WordClassResponse(BaseResponse):
    id: int
    name: str
    abbreviation: str
    part_of_speech: str
    language_id: int


class WordResponse(BaseResponse):
    id: int
    word: str
    part_of_speech: str
    notes: str | None

    word_links: list[WordLinkResponse]
    word_classes: list[WordClassResponse]

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


class GrammarTableCategoryResponse(BaseResponse):
    id: int
    content: list[str]

    @field_validator("content", mode="before")
    @classmethod
    def convert_json_to_list(cls, value: str) -> list[str]:
        try:
            output = json.loads(value)
            if not isinstance(output, list):
                raise ValidationError()
            return output
        except Exception:
            raise ValidationError()


class GrammarTableCellResponse(BaseResponse):
    id: int

    row_categories: list[str]
    column_categories: list[str]

    @field_validator("row_categories", "column_categories", mode="before")
    @classmethod
    def convert_json_to_list(cls, value: str) -> list[str]:
        try:
            output = json.loads(value)
            if not isinstance(output, list):
                raise ValidationError()
            return output
        except Exception:
            raise ValidationError()


class GrammarTableResponse(BaseResponse):
    id: int
    name: str
    part_of_speech: str
    language_id: int

    word_classes: list[WordClassResponse]

    rows: list[GrammarTableCategoryResponse]
    columns: list[GrammarTableCategoryResponse]

    cells: list[GrammarTableCellResponse]
