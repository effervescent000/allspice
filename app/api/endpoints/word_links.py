from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User, WordLink
from app.schemas.requests import WordLinkRequest
from app.schemas.responses import WordLinkResponse

router = APIRouter()


@router.post("/", response_model=list[WordLinkResponse])
async def upsert_word_links(
    word_links: list[WordLinkRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    new_word_links = [WordLink(**word_link.model_dump()) for word_link in word_links]
    session.add_all(new_word_links)
    await session.commit()
    return new_word_links


@router.get("/", response_model=list[WordLinkResponse])
async def get_word_links(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(select(WordLink).order_by(WordLink.definition))
    word_links = result.scalars().all()
    return word_links


@router.delete("/{word_link_id}", status_code=204)
async def delete_word_link(
    word_link_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    await session.execute(delete(WordLink).where(WordLink.id == word_link_id))
    await session.commit()
