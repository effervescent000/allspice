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
    word_classes: list[int] = None,
):
    return {
        **base_word_factory(
            id=id, word=word, part_of_speech=part_of_speech, language_id=language_id
        ),
        "word_link_ids": word_links or [],
        "word_class_ids": word_classes or [],
    }


def word_response_factory(
    id: int = None,
    *,
    word: str = None,
    part_of_speech: str = None,
    language_id: int = None,
    word_links: list[dict[str, Any]] = None,
    word_classes: list[dict[str, Any]] = None,
):
    return {
        **base_word_factory(
            id=id, word=word, part_of_speech=part_of_speech, language_id=language_id
        ),
        "word_links": word_links or [],
        "word_classes": word_classes or [],
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


def word_class_factory(
    id: int = None,
    *,
    name: str = None,
    abbreviation: str = None,
    part_of_speech: str = None,
    language_id: int,
):
    return {
        "id": id,
        "name": name or "test word class",
        "abbreviation": abbreviation or "twc",
        "part_of_speech": part_of_speech or "verb",
        "language_id": language_id,
    }


def grammar_category_factory(id: int = None, *, content: list[str]):
    return {"id": id, "content": content}


def grammar_table_base_factory(
    id: int = None, *, name: str = None, language_id: int, part_of_speech: str = None
):
    return {
        "id": id,
        "name": name or "test table",
        "part_of_speech": part_of_speech or "verb",
        "language_id": language_id,
    }


def grammar_table_request_factory(
    id: int = None,
    *,
    name: str = None,
    language_id: int,
    part_of_speech: str = None,
    word_class_ids: list[str] = None,
):
    return {
        **grammar_table_base_factory(
            id=id, name=name, language_id=language_id, part_of_speech=part_of_speech
        ),
        "word_class_ids": word_class_ids,
    }


def grammar_cell_factory(
    id: int = None, *, row_categories: list[str], column_categories: list[str]
):
    return {
        "id": id,
        "row_categories": row_categories,
        "column_categories": column_categories,
    }
