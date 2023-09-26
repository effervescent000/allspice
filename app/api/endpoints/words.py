from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Language, User, Word
from app.schemas.requests import WordRequest
from app.schemas.responses import WordResponse

router = APIRouter()


@router.get("/by_language/{language_id}", response_model=list[WordResponse])
async def get_all_words(
    language_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(
        select(Word)
        .where(Word.language_id == language_id)
        .where(Language.user_id == current_user.id)
        .join(Language)
    )
    words = result.unique().scalars().all()
    return words


@router.post("/", response_model=list[WordResponse])
async def upsert_words(
    words: list[WordRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    ...
    # first, validate that the language in question belongs to the user
