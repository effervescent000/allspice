from httpx import AsyncClient

from app.main import app
from app.models import Language, Word
from app.tests.shapes import word_link_factory, word_response_factory


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
    assert words == [
        word_response_factory(
            id=default_word.id,
            language_id=default_language.id,
            word_links=[word_link_factory(id=1)],
        )
    ]
