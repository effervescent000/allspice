from httpx import AsyncClient

from app.main import app
from app.models import Language
from app.tests.shapes import sound_change_rules_factory


async def test_sca(
    client: AsyncClient, default_user_headers, default_sound_change_rules
):
    response = await client.post(
        app.url_path_for("sca"),
        headers=default_user_headers,
        json=[
            {"sound_changes_id": default_sound_change_rules.id, "word_list": ["test"]}
        ],
    )
    content = response.json()["output"]
    assert content == ["tast"]


async def test_upsert_sound_changes(
    client: AsyncClient, default_user_headers, default_language: Language
):
    response = await client.post(
        app.url_path_for("upsert_sound_changes"),
        headers=default_user_headers,
        json=[
            sound_change_rules_factory(
                content="new-rule:\nunchanged", language_id=default_language.id
            )
        ],
    )
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"] == "new-rule:\nunchanged"
