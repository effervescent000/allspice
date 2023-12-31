from typing import Literal

from pydantic import BaseModel, field_validator


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
    word_class_ids: list[int] = []


class PhoneRequest(BaseRequest):
    id: int | None = None
    base_phone: str
    quality: str | None = None
    graph: str | None = None
    vowel: bool | None = False
    language_id: int

    @field_validator("graph", "quality")
    @classmethod
    def nullify_empty_strings(cls, v: str | None) -> str | None:
        if v == "":
            return None
        return v


class PhonologyRequest(BaseRequest):
    phonology: list[PhoneRequest]
    mode: Literal["insert", "replace"]


class SCInput(BaseRequest):
    word_list: list[str]
    sound_changes_id: int


class SoundChangeRulesRequest(BaseRequest):
    id: int | None = None
    name: str | None = None
    content: str
    role: str | None = None
    language_id: int


class WordClassRequest(BaseRequest):
    id: int | None = None
    name: str
    abbreviation: str
    part_of_speech: str
    language_id: int


class GrammarTableCategoryRequest(BaseRequest):
    id: int | None = None
    content: list[str]


class GrammarTableCellRequest(BaseRequest):
    id: int | None = None

    row_categories: list[str]
    column_categories: list[str]

    sound_change_rules: SoundChangeRulesRequest


class GrammarTableRequest(BaseRequest):
    id: int | None = None
    name: str
    part_of_speech: str
    language_id: int

    word_class_ids: list[int] = []

    rows: list[GrammarTableCategoryRequest]
    columns: list[GrammarTableCategoryRequest]

    cells: list[GrammarTableCellRequest]
