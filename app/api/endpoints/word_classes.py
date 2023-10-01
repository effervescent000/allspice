from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User, WordClass
from app.schemas.requests import WordClassRequest
from app.schemas.responses import WordClassResponse
from app.utils.db_utils import verify_ownership

router = APIRouter()


@router.post("/", response_model=list[WordClassResponse])
async def upsert_word_classes(
    word_classes: list[WordClassRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    await verify_ownership(
        session,
        current_user=current_user,
        schema=WordClass,
        target_ids=[x.id for x in word_classes if x.id is not None],
    )

    upserted = []
    for word_class in word_classes:
        merged = await session.merge(WordClass(**word_class.model_dump()))
        upserted.append(merged)
    await session.commit()
    return upserted


@router.get("/by_language/{language_id}", response_model=list[WordClassResponse])
async def get_all_word_classes_by_language(
    language_id: int,
    current_user: User = (Depends(deps.get_current_user)),
    session: AsyncSession = (Depends(deps.get_session)),
):
    word_classes = (
        await session.scalars(
            select(WordClass).where(WordClass.language_id == language_id)
        )
    ).all()

    await verify_ownership(
        session,
        current_user=current_user,
        schema=WordClass,
        target_ids=[x.id for x in word_classes],
    )

    return word_classes
