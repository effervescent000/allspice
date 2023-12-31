from httpx import AsyncClient

from app.main import app
from app.models import Language, Word, WordClass, WordLink
from app.tests.shapes import (
    prune_fields,
    word_class_factory,
    word_link_factory,
    word_request_factory,
    word_response_factory,
)


async def test_get_words(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word: Word,
    second_word,
):
    response = await client.get(
        app.url_path_for("get_all_words", language_id=default_language.id),
        headers=default_user_headers,
    )
    words = response.json()
    assert len(words) == 1
    assert prune_fields(data=words, fields=["id"], nest=["word_links"]) == prune_fields(
        data=[
            word_response_factory(
                language_id=default_language.id,
                word_links=[word_link_factory(id=1)],
            )
        ],
        fields=["id"],
        nest=["word_links"],
    )


async def test_upsert_words_create_word(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word_link: WordLink,
    default_word_class: WordClass,
):
    response = await client.post(
        app.url_path_for("upsert_words"),
        headers=default_user_headers,
        json=[
            word_request_factory(
                language_id=default_language.id,
                word_links=[default_word_link.id],
                word_classes=[default_word_class.id],
            )
        ],
    )
    words = response.json()
    assert len(words) == 1
    assert prune_fields(data=words, nest=["word_classes"]) == prune_fields(
        data=[
            word_response_factory(
                id=1,
                language_id=default_language.id,
                word_links=[word_link_factory(id=default_word_link.id)],
                word_classes=[
                    word_class_factory(
                        name="default word class",
                        abbreviation="dwc",
                        language_id=default_language.id,
                    )
                ],
            )
        ],
        nest=["word_classes"],
    )


async def test_upsert_words_add_word_link(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word: Word,
    default_word_link: WordLink,
    secondary_word_link: WordLink,
):
    response = await client.post(
        app.url_path_for("upsert_words"),
        headers=default_user_headers,
        json=[
            word_request_factory(
                id=default_word.id,
                language_id=default_language.id,
                word_links=[default_word_link.id, secondary_word_link.id],
            )
        ],
    )
    words = response.json()
    assert len(words) == 1
    assert words == [
        word_response_factory(
            id=default_word.id,
            language_id=default_language.id,
            word_links=[
                word_link_factory(id=default_word_link.id),
                word_link_factory(id=secondary_word_link.id, definition="new"),
            ],
        )
    ]


async def test_upsert_words_alter_word_classes(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word: Word,
    default_word_class: WordClass,
    secondary_word_class: WordClass,
):
    """Add a word class and remove another."""
    response = await client.post(
        app.url_path_for("upsert_words"),
        headers=default_user_headers,
        json=[
            word_request_factory(
                id=default_word.id,
                language_id=default_language.id,
                word_classes=[secondary_word_class.id],
            )
        ],
    )
    words = response.json()
    assert len(words) == 1
    assert len(words[0]["word_classes"]) == 1
    assert words == [
        word_response_factory(
            id=default_word.id,
            language_id=default_language.id,
            word_links=[],
            word_classes=[
                word_class_factory(
                    id=secondary_word_class.id,
                    name="secondary word class",
                    abbreviation="swc",
                    language_id=default_language.id,
                )
            ],
        )
    ]


async def test_delete_word(
    client: AsyncClient,
    default_user_headers,
    default_word: Word,
):
    response = await client.delete(
        app.url_path_for("delete_word", word_id=default_word.id),
        headers=default_user_headers,
    )
    assert response.status_code == 204
