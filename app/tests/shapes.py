def word_link_factory(
    id: int = None,
    *,
    definition: str = None,
    hint: str = None,
    part_of_speech: str = None
):
    return {
        "id": id,
        "definition": definition or "test",
        "hint": hint,
        "part_of_speech": part_of_speech or "verb",
    }


def word_factory(
    id: int = None,
    *,
    word: str = None,
    part_of_speech: str = None,
    language_id: int = None
):
    return {
        "id": id,
        "word": word or "teeeeeeeest",
        "part_of_speech": part_of_speech or "noun",
        "language_id": language_id or 1,
    }
