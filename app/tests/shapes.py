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
