from httpx import AsyncClient

from app.main import app


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
