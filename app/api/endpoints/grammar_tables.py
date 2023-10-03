import json

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import (
    GrammarTable,
    GrammarTableCell,
    GrammarTableColumn,
    GrammarTableRow,
    Language,
    User,
    WordClass,
)
from app.schemas.requests import GrammarTableRequest
from app.schemas.responses import GrammarTableFullResponse, GrammarTableMinimalResponse
from app.utils.db_utils import verify_ownership

router = APIRouter()


@router.get("/{language_id}", response_model=list[GrammarTableMinimalResponse])
async def get_grammar_tables_by_language(
    language_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    tables = (
        (
            await session.scalars(
                select(GrammarTable)
                .where(
                    GrammarTable.language_id == language_id,
                    Language.user_id == current_user.id,
                )
                .options()
                .join(Language)
            )
        )
        .unique()
        .all()
    )
    return tables


@router.post("/", response_model=list[GrammarTableFullResponse])
async def upsert_grammar_tables(
    grammar_tables: list[GrammarTableRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    found_ids = {x.id for x in grammar_tables if x.id is not None}

    await verify_ownership(
        session, current_user=current_user, schema=GrammarTable, target_ids=found_ids
    )

    upserted = []
    for table in grammar_tables:
        word_class_ids = table.word_class_ids

        to_upsert = GrammarTable(
            **table.model_dump(exclude=["word_class_ids", "rows", "columns", "cells"])
        )

        rows = [
            GrammarTableRow(
                **x.model_dump(exclude=["content"]), content=json.dumps(x.content)
            )
            for x in table.rows
        ]
        columns = [
            GrammarTableColumn(
                **x.model_dump(exclude=["content"]), content=json.dumps(x.content)
            )
            for x in table.columns
        ]
        cells = [
            GrammarTableCell(
                **x.model_dump(exclude=["row_categories", "column_categories"]),
                row_categories=json.dumps(x.row_categories),
                column_categories=json.dumps(x.column_categories)
            )
            for x in table.cells
        ]

        word_classes = (
            await session.scalars(
                select(WordClass).where(WordClass.id.in_(word_class_ids))
            )
        ).all()
        to_upsert.word_classes = word_classes
        to_upsert.rows = rows
        to_upsert.columns = columns
        to_upsert.cells = cells

        merged = await session.merge(to_upsert)

        upserted.append(merged)
    await session.commit()
    return upserted
