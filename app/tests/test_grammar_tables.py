from httpx import AsyncClient

from app.main import app
from app.models import GrammarTable, Language, WordClass
from app.tests.shapes import (
    grammar_category_factory,
    grammar_cell_factory,
    grammar_table_base_factory,
    grammar_table_request_factory,
    prune_fields,
    word_class_factory,
)


async def test_upsert_grammar_tables(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_word_class: WordClass,
):
    response = await client.post(
        app.url_path_for("upsert_grammar_tables"),
        headers=default_user_headers,
        json=[
            {
                **grammar_table_request_factory(language_id=default_language.id),
                "word_class_ids": [default_word_class.id],
                "rows": [grammar_category_factory(content=["test"])],
                "columns": [grammar_category_factory(content=["another"])],
                "cells": [
                    grammar_cell_factory(
                        row_categories=["test"], column_categories=["another"]
                    )
                ],
            }
        ],
    )
    json = response.json()
    assert len(json) == 1
    assert isinstance(json[0]["id"], int)
    assert prune_fields(
        data=json, nest=["rows", "columns", "cells", "word_classes"]
    ) == prune_fields(
        data=[
            {
                **grammar_table_base_factory(language_id=default_language.id),
                "rows": [grammar_category_factory(content=["test"])],
                "columns": [grammar_category_factory(content=["another"])],
                "cells": [
                    grammar_cell_factory(
                        row_categories=["test"], column_categories=["another"]
                    )
                ],
                "word_classes": [
                    word_class_factory(
                        name="default word class",
                        abbreviation="dwc",
                        language_id=default_language.id,
                    )
                ],
            }
        ],
        nest=["rows", "columns", "cells", "word_classes"],
    )


async def test_get_grammar_tables_by_language(
    client: AsyncClient,
    default_user_headers,
    default_language: Language,
    default_grammar_table: GrammarTable,
):
    response = await client.get(
        app.url_path_for(
            "get_grammar_tables_by_language", language_id=default_language.id
        ),
        headers=default_user_headers,
    )

    json = response.json()
    assert len(json) == 1
    assert isinstance(json[0]["id"], int)
    assert prune_fields(data=json) == prune_fields(
        data=[
            {
                **grammar_table_base_factory(
                    language_id=default_language.id, name="default grammar table"
                ),
            }
        ],
    )
