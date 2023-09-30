from httpx import AsyncClient

from app.main import app
from app.models import Language, SoundChangeRules, Word
from app.tests.shapes import sound_change_rules_factory


async def test_sca_with_words(
    client: AsyncClient,
    default_user_headers,
    default_sound_change_rules: SoundChangeRules,
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


async def test_sca_with_ids(
    client: AsyncClient,
    default_user_headers,
    default_sound_change_rules: SoundChangeRules,
    default_word: Word,
):
    response = await client.post(
        app.url_path_for("sca"),
        headers=default_user_headers,
        json=[
            {
                "sound_changes_id": default_sound_change_rules.id,
                "word_list": [str(default_word.id)],
            }
        ],
    )
    content = response.json()["output"]
    assert content == ["taaaaaaaast"]


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


async def test_upsert_sound_changes_dont_duplicate_spelling(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    spelling_sound_change_rules: SoundChangeRules,
):
    await client.post(
        app.url_path_for("upsert_sound_changes"),
        headers=default_user_headers,
        json=[
            sound_change_rules_factory(
                id=spelling_sound_change_rules.id,
                content="new-rule:\nunchanged",
                language_id=default_language.id,
                role="spelling",
            )
        ],
    )

    get_response = await client.get(
        app.url_path_for("read_sound_changes"),
        headers=default_user_headers,
        params={"role": "spelling"},
    )

    rules = get_response.json()
    assert len(rules) == 1


async def test_get_sc_with_role(
    client: AsyncClient,
    default_user_headers,
    default_sound_change_rules: SoundChangeRules,
    spelling_sound_change_rules: SoundChangeRules,
):
    response = await client.get(
        app.url_path_for("read_sound_changes"),
        headers=default_user_headers,
        params={"role": "spelling"},
    )
    rules = response.json()
    assert len(rules) == 1
    assert rules[0]["role"] == "spelling"


async def test_get_sc_without_role(
    client: AsyncClient,
    default_user_headers,
    default_sound_change_rules: SoundChangeRules,
    spelling_sound_change_rules: SoundChangeRules,
):
    response = await client.get(
        app.url_path_for("read_sound_changes"),
        headers=default_user_headers,
    )
    rules = response.json()
    assert len(rules) == 2
