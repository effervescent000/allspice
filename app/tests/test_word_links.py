from httpx import AsyncClient

from app.main import app
from app.tests.shapes import word_link_factory

WORD_LINK_WORD = "test"


async def test_upsert_word_links(client: AsyncClient, default_user_headers):
    dummy_word_link = word_link_factory(definition=WORD_LINK_WORD)
    response = await client.post(
        app.url_path_for("upsert_word_links"),
        headers=default_user_headers,
        json=[dummy_word_link],
    )
    assert response.status_code == 200
    word_links = response.json()
    assert len(word_links) == 1
    assert word_links[0] == {**dummy_word_link | {"id": 1}}
