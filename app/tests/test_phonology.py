from httpx import AsyncClient

from app.main import app
from app.models import Language
from app.tests.shapes import phone_factory, prune_fields


async def test_upsert_phones(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
):
    response = await client.post(
        app.url_path_for("upsert_phones"),
        headers=default_user_headers,
        json=[phone_factory(language_id=default_language.id)],
    )
    phones = response.json()
    assert len(phones) == 1
    assert prune_fields(data=phones) == prune_fields(
        data=[
            {
                **phone_factory(id=1, language_id=default_language.id),
                "composed_phone": "k",
            }
        ]
    )
