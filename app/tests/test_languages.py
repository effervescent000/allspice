from httpx import AsyncClient

from app.main import app

LANGUAGE_NAME = "test language"
LANGUAGE_DESCRIPTION = "fake description"


async def test_upsert_language(client: AsyncClient, default_user_headers):
    response = await client.post(
        app.url_path_for("upsert_language"),
        json=[{"name": LANGUAGE_NAME, "description": LANGUAGE_DESCRIPTION}],
        headers=default_user_headers,
    )
    assert response.status_code == 200
    language = response.json()
    assert language["name"] == LANGUAGE_NAME
    assert language["description"] == LANGUAGE_DESCRIPTION
