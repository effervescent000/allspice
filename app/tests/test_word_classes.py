from httpx import AsyncClient

from app.main import app
from app.models import Language
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
