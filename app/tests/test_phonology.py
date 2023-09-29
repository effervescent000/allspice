from httpx import AsyncClient

from app.main import app
from app.models import Language, Phone
from app.tests.shapes import phone_factory, prune_fields


async def test_upsert_phones_insert_only(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
):
    response = await client.post(
        app.url_path_for("upsert_phones"),
        headers=default_user_headers,
        json=[
            {
                "phonology": [phone_factory(language_id=default_language.id)],
                "mode": "insert",
            }
        ],
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


async def test_upsert_phones_replace(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_phone: Phone,
):
    response = await client.post(
        app.url_path_for("upsert_phones"),
        headers=default_user_headers,
        json=[
            {
                "phonology": [
                    phone_factory(language_id=default_language.id, base_phone="p")
                ],
                "mode": "replace",
            }
        ],
    )
    phones = response.json()
    assert len(phones) == 1
    assert phones[0]["id"] != default_phone.id


async def test_get_phones(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_phone: Phone,
):
    response = await client.get(
        app.url_path_for("get_language_phones", language_id=default_language.id),
        headers=default_user_headers,
    )
    phones = response.json()
    assert len(phones) == 1
    assert phones == [
        {
            **phone_factory(id=1001, base_phone="k", language_id=default_language.id),
            "composed_phone": "k",
        }
    ]


async def test_delete_phone(
    client: AsyncClient,
    default_user_headers,
    default_phone: Phone,
):
    response = await client.delete(
        app.url_path_for("delete_phone", phone_id=default_phone.id),
        headers=default_user_headers,
    )
    assert response.status_code == 204
