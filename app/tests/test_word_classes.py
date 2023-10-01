from httpx import AsyncClient

from app.main import app
from app.models import Language, WordClass
from app.tests.shapes import prune_fields, word_class_factory


async def test_upsert_word_classes(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
):
    response = await client.post(
        app.url_path_for("upsert_word_classes"),
        headers=default_user_headers,
        json=[word_class_factory(language_id=default_language.id)],
    )
    word_classes = response.json()
    assert len(word_classes) == 1
    word_class_id = word_classes[0].pop("id")
    assert isinstance(word_class_id, int)
    assert word_classes == prune_fields(
        data=[word_class_factory(language_id=default_language.id)], fields=["id"]
    )


async def test_get_all_word_classes(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word_class: WordClass,
):
    response = await client.get(
        app.url_path_for(
            "get_all_word_classes_by_language", language_id=default_language.id
        ),
        headers=default_user_headers,
    )
    word_classes = response.json()
    assert len(word_classes) == 1
    assert prune_fields(data=word_classes) == prune_fields(
        data=[
            word_class_factory(
                name="default word class",
                abbreviation="dwc",
                language_id=default_language.id,
            )
        ]
    )
