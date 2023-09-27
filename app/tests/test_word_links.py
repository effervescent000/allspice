from httpx import AsyncClient

from app.main import app
from app.tests.shapes import word_link_factory

WORD_LINK_WORD = "test"


async def test_upsert_word_links(client: AsyncClient, default_user_headers):
    dummy_word_link = word_link_factory(definition=WORD_LINK_WORD, id=1000)
    response = await client.post(
        app.url_path_for("upsert_word_links"),
        headers=default_user_headers,
        json=[dummy_word_link],
    )
    word_links = response.json()
    assert len(word_links) == 1
    assert word_links[0] == {**dummy_word_link}


async def test_get_word_links(
    client: AsyncClient, default_user_headers, default_word_link
):
    response = await client.get(
        app.url_path_for("get_word_links"), headers=default_user_headers
    )
    word_links = response.json()
    assert len(word_links) == 1
    assert word_links == [word_link_factory(id=default_word_link.id, definition="test")]


async def test_delete_word_link(
    client: AsyncClient, default_user_headers, default_word_link
):
    response = await client.delete(
        app.url_path_for("delete_word_link", word_link_id=1),
        headers=default_user_headers,
    )
    assert response.status_code == 204
