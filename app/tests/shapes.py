from typing import Any


def prune_fields(
    *, data: list[dict[str, Any]], fields: list[str] = ["id"], nest: list[str] = []
):
    for x in data:
        for field in fields:
            x.pop(field)
        for field in nest:
            if x.get(field):
                x[field] = prune_fields(data=x[field], fields=["id"])
    return data


def word_link_factory(
    id: int = None,
    *,
    definition: str = None,
    hint: str = None,
    part_of_speech: str = None,
):
    return {
        "id": id,
        "definition": definition or "test",
        "hint": hint,
        "part_of_speech": part_of_speech or "verb",
    }


def base_word_factory(
    id: int = None,
    *,
    word: str = None,
    part_of_speech: str = None,
    language_id: int = None,
    notes: str = None,
):
    return {
        "id": id,
        "word": word or "teeeeeeeest",
        "part_of_speech": part_of_speech or "noun",
        "language_id": language_id or 1,
        "notes": notes,
    }


def word_request_factory(
    id: int = None,
    *,
    word: str = None,
    part_of_speech: str = None,
    language_id: int = None,
    word_links: list[int] = None,
):
    return {
        **base_word_factory(
            id=id, word=word, part_of_speech=part_of_speech, language_id=language_id
        ),
        "word_link_ids": word_links,
    }


def word_response_factory(
    id: int = None,
    *,
    word: str = None,
    part_of_speech: str = None,
    language_id: int = None,
    word_links: list[dict[str, Any]] = None,
):
    return {
        **base_word_factory(
            id=id, word=word, part_of_speech=part_of_speech, language_id=language_id
        ),
        "word_links": word_links,
    }


def phone_factory(
    id: int = None,
    *,
    base_phone: str = None,
    quality: str = None,
    graph: str = None,
    vowel: bool = None,
    language_id: int,
):
    return {
        "id": id,
        "base_phone": base_phone or "k",
        "quality": quality,
        "graph": graph,
        "vowel": vowel or False,
        "language_id": language_id,
    }


def sound_change_rules_factory(
    id: int = None,
    *,
    content: str = None,
    language_id: int,
    name: str = None,
    role: str = None,
):
    return {
        "id": id,
        "content": content or "dummy-rule:\ne => a",
        "language_id": language_id,
        "name": name,
        "role": role,
    }
