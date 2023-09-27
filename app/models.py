"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from app.utils.utils import QUALITY_DIACRITIC_LOOKUP, get_now_int


class Base(DeclarativeBase):
    pass


class AuditTimestamps:
    created_at: Mapped[int] = mapped_column(default=get_now_int)
    updated_at: Mapped[int] = mapped_column(default=get_now_int, onupdate=get_now_int)


class LanguageRelated:
    language_id: Mapped[int] = mapped_column(
        ForeignKey("language_model.id", ondelete="CASCADE")
    )

    @declared_attr
    def language(self) -> Mapped["Language"]:
        return relationship("Language", viewonly=True)


class User(AuditTimestamps, Base):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    languages: Mapped[list["Language"]] = relationship(
        back_populates="user", cascade="delete, delete-orphan"
    )


class Language(AuditTimestamps, Base):
    __tablename__ = "language_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    user_id: Mapped[str] = mapped_column(
        ForeignKey("user_model.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="languages")
    words: Mapped[list["Word"]] = relationship()


word_link_to_word = Table(
    "word_link_to_word",
    Base.metadata,
    Column(
        "word_link_id",
        ForeignKey("word_link_model.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "word_id", ForeignKey("word_model.id", ondelete="CASCADE"), primary_key=True
    ),
)


class WordLink(AuditTimestamps, Base):
    __tablename__ = "word_link_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    definition: Mapped[str]
    hint: Mapped[str | None]
    part_of_speech: Mapped[str]

    words: Mapped[list["Word"]] = relationship(
        secondary=word_link_to_word, back_populates="word_links"
    )


class Word(AuditTimestamps, LanguageRelated, Base):
    __tablename__ = "word_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    part_of_speech: Mapped[str]
    notes: Mapped[str | None]

    word_links: Mapped[list["WordLink"]] = relationship(
        secondary=word_link_to_word, back_populates="words", lazy="joined"
    )


class Phone(LanguageRelated, Base):
    __tablename__ = "phone_model"

    id: Mapped[int] = mapped_column(primary_key=True)

    base_phone: Mapped[str] = mapped_column(String(10))
    quality: Mapped[str | None]
    graph: Mapped[str | None]
    vowel: Mapped[bool]

    @property
    def composed_phone(self):
        return (
            self.base_phone + QUALITY_DIACRITIC_LOOKUP[self.quality]
            if self.quality
            else self.base_phone
        )
