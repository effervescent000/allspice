import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, security
from app.core.session import async_engine, async_session
from app.main import app
from app.models import (
    Base,
    GrammarTable,
    GrammarTableCell,
    GrammarTableColumn,
    GrammarTableRow,
    Language,
    ORMType,
    Phone,
    SoundChangeRules,
    User,
    Word,
    WordClass,
    WordLink,
)
from app.tests.shapes import (
    base_word_factory,
    grammar_category_factory,
    grammar_cell_factory,
    grammar_table_base_factory,
    phone_factory,
    sound_change_rules_factory,
    word_class_factory,
    word_link_factory,
)

default_user_id = "b75365d9-7bf9-4f54-add5-aeab333a087b"
default_user_email = "geralt@wiedzmin.pl"
default_user_password = "geralt"
default_user_password_hash = security.get_password_hash(default_user_password)
default_user_access_token = security.create_jwt_token(
    str(default_user_id), 60 * 60 * 24, refresh=False
)[0]
default_language_name = "test language"
secondary_language_name = "second language"
default_word_link_def = "test"
default_word_link_id = 1001
secondary_word_link_def = "new"
default_word_name = "teeeeeeeest"
secondary_word_name = "new word"
default_phone_name = "k"
default_word_class_name = "default word class"
default_word_class_abbr = "dwc"
secondary_word_class_name = "secondary word class"
secondary_word_class_abbr = "swc"
default_grammar_table_name = "default grammar table"


async def get_or_insert_model(
    schema: ORMType,
    search_field: str,
    search_value: str,
    factory_output: dict[str, Any],
):
    async with async_session() as session:
        result = (
            await session.scalars(
                select(schema).where(getattr(schema, search_field) == search_value)
            )
        ).first()
        if result is None:
            input = schema(**factory_output)
            session.add(input)
            await session.commit()
            await session.refresh(input)
            return input
        return result


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

        # delete all data from all tables after test
        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture
async def default_user(test_db_setup_sessionmaker) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.username == default_user_email)
        )
        user = result.scalars().first()
        if user is None:
            new_user = User(
                username=default_user_email,
                hashed_password=default_user_password_hash,
            )
            new_user.id = default_user_id
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        return user


@pytest.fixture
def default_user_headers(default_user: User):
    return {"Authorization": f"Bearer {default_user_access_token}"}


@pytest_asyncio.fixture
async def default_language(test_db_setup_sessionmaker) -> Language:
    async with async_session() as session:
        result = await session.execute(
            select(Language).where(Language.name == default_language_name)
        )
        language = result.scalars().first()
        if language is None:
            new_language = Language(
                name=default_language_name,
                description="test description",
                user_id=default_user_id,
            )
            session.add(new_language)
            await session.commit()
            await session.refresh(new_language)
            return new_language
        return language


@pytest_asyncio.fixture
async def default_phone(
    test_db_setup_sessionmaker, default_language: Language
) -> Phone:
    async with async_session() as session:
        phone = (
            await session.scalars(
                select(Phone)
                .where(Phone.base_phone == default_phone_name)
                .where(Phone.language_id == default_language.id)
            )
        ).first()
        if phone is None:
            new_phone = Phone(
                **phone_factory(
                    id=1001, base_phone="k", language_id=default_language.id
                )
            )
            session.add(new_phone)
            await session.commit()
            await session.refresh(new_phone)
            return new_phone
        return phone


@pytest_asyncio.fixture
async def second_language(test_db_setup_sessionmaker) -> Language:
    async with async_session() as session:
        result = await session.execute(
            select(Language).where(Language.name == secondary_language_name)
        )
        language = result.scalars().first()
        if language is None:
            new_language = Language(
                name=secondary_language_name,
                description="test description",
                user_id=default_user_id,
            )
            session.add(new_language)
            await session.commit()
            await session.refresh(new_language)
            return new_language
        return language


@pytest_asyncio.fixture
async def default_word_link(test_db_setup_sessionmaker) -> WordLink:
    async with async_session() as session:
        result = await session.execute(
            select(WordLink).where(WordLink.id == default_word_link_id)
        )
        word_link = result.scalars().first()
        if word_link is None:
            new_word_link = WordLink(
                **word_link_factory(
                    definition=default_word_link_def, id=default_word_link_id
                )
            )
            session.add(new_word_link)
            await session.commit()
            await session.refresh(new_word_link)
            return new_word_link
    return word_link


@pytest_asyncio.fixture
async def secondary_word_link(test_db_setup_sessionmaker) -> WordLink:
    async with async_session() as session:
        result = await session.execute(
            select(WordLink).where(WordLink.definition == secondary_word_link_def)
        )
        word_link = result.scalars().first()
        if word_link is None:
            new_word_link = WordLink(
                **word_link_factory(definition=secondary_word_link_def)
            )
            session.add(new_word_link)
            await session.commit()
            await session.refresh(new_word_link)
            return new_word_link
    return word_link


@pytest_asyncio.fixture
async def default_word(
    test_db_setup_sessionmaker, default_word_link: WordLink, default_language: Language
) -> Word:
    async with async_session() as session:
        result = await session.execute(
            select(Word).where(Word.word == default_word_name)
        )
        word_def = result.scalars().first()
        if word_def is None:
            new_word = Word(
                **base_word_factory(
                    word=default_word_name,
                    language_id=default_language.id,
                )
            )
            new_word.word_links.append(default_word_link)
            session.add(new_word)
            await session.commit()
            await session.refresh(new_word)
            return new_word
        return word_def


@pytest_asyncio.fixture
async def second_word(
    test_db_setup_sessionmaker, default_word_link: WordLink, second_language: Language
) -> Word:
    async with async_session() as session:
        result = await session.execute(
            select(Word).where(Word.word == secondary_word_name)
        )
        word_def = result.scalars().first()
        if word_def is None:
            new_word = Word(
                **base_word_factory(
                    word=secondary_word_name,
                    language_id=second_language.id,
                )
            )
            new_word.word_links.append(default_word_link)
            session.add(new_word)
            await session.commit()
            await session.refresh(new_word)
            return new_word
        return word_def


@pytest_asyncio.fixture
async def default_sound_change_rules(
    test_db_setup_sessionmaker, default_language: Language
) -> SoundChangeRules:
    async with async_session() as session:
        sound_change_rules = (
            await session.scalars(
                select(SoundChangeRules).where(
                    SoundChangeRules.language_id == default_language.id
                )
            )
        ).first()
        if sound_change_rules is None:
            new_rules = SoundChangeRules(
                **sound_change_rules_factory(language_id=default_language.id)
            )
            session.add(new_rules)
            await session.commit()
            await session.refresh(new_rules)
            return new_rules
        return sound_change_rules


@pytest_asyncio.fixture
async def spelling_sound_change_rules(
    test_db_setup_sessionmaker, default_language: Language
) -> SoundChangeRules:
    async with async_session() as session:
        sound_change_rules = (
            await session.scalars(
                select(SoundChangeRules)
                .where(SoundChangeRules.language_id == default_language.id)
                .where(SoundChangeRules.role == "spelling")
            )
        ).first()
        if sound_change_rules is None:
            new_rules = SoundChangeRules(
                **sound_change_rules_factory(
                    language_id=default_language.id, role="spelling"
                )
            )
            session.add(new_rules)
            await session.commit()
            await session.refresh(new_rules)
            return new_rules
        return sound_change_rules


@pytest_asyncio.fixture
async def default_word_class(
    test_db_setup_sessionmaker, default_language: Language
) -> WordClass:
    async with async_session() as session:
        word_class = (
            await session.scalars(
                select(WordClass)
                .where(WordClass.language_id == default_language.id)
                .where(WordClass.name == default_word_class_name)
            )
        ).first()
        if word_class is None:
            new = WordClass(
                **word_class_factory(
                    language_id=default_language.id,
                    name=default_word_class_name,
                    abbreviation=default_word_class_abbr,
                )
            )
            session.add(new)
            await session.commit()
            await session.refresh(new)
            return new
        return word_class


@pytest_asyncio.fixture
async def secondary_word_class(
    test_db_setup_sessionmaker, default_language: Language
) -> WordClass:
    return await get_or_insert_model(
        schema=WordClass,
        search_field="name",
        search_value=secondary_word_class_name,
        factory_output=word_class_factory(
            name=secondary_word_class_name,
            abbreviation=secondary_word_class_abbr,
            language_id=default_language.id,
        ),
    )


@pytest_asyncio.fixture
async def default_grammar_table(
    test_db_setup_sessionmaker,
    default_language: Language,
    default_word_class: WordClass,
    default_sound_change_rules: SoundChangeRules,
) -> GrammarTable:
    async with async_session() as session:
        table = (
            await session.scalars(
                select(GrammarTable).where(
                    GrammarTable.name == default_grammar_table_name
                )
            )
        ).first()
        if table is None:
            new_table = GrammarTable(
                **grammar_table_base_factory(
                    language_id=default_language.id, name=default_grammar_table_name
                ),
                word_classes=[default_word_class],
                rows=[GrammarTableRow(**grammar_category_factory(content='["test"]'))],
                columns=[
                    GrammarTableColumn(
                        **grammar_category_factory(content='["another"]')
                    )
                ],
                cells=[
                    GrammarTableCell(
                        **grammar_cell_factory(
                            row_categories='["test"]',
                            column_categories='["another"]',
                            sound_change_rules=SoundChangeRules(
                                **sound_change_rules_factory(
                                    language_id=default_language.id
                                )
                            ),
                        )
                    )
                ],
            )
            session.add(new_table)
            await session.commit()
            await session.refresh(new_table)
            return new_table
        return table
