from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api import deps
from app.models import Language, User, Word, WordClass, WordLink
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
        .order_by(Word.word)
    )
    words = result.unique().scalars().all()
    return words


@router.post("/", response_model=list[WordResponse])
async def upsert_words(
    words: list[WordRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    # first, verify that the user upserting owns the language in question
    language_ids = {word.language_id for word in words}
    if len(language_ids) > 1:
        raise HTTPException(status_code=400, detail="Too many languages")

    language = (
        (await session.execute(select(Language).where(Language.id.in_(language_ids))))
        .scalars()
        .first()
    )
    if language.user_id != current_user.id:
        raise HTTPException(status_code=401)

    # now upsert
    output = []
    for word in words:
        word_links = (
            (
                await session.scalars(
                    select(WordLink).where(WordLink.id.in_(word.word_link_ids))
                )
            )
            .unique()
            .all()
        )
        word_classes = (
            (
                await session.scalars(
                    select(WordClass).where(WordClass.id.in_(word.word_class_ids))
                )
            )
            .unique()
            .all()
        )

        word_to_upsert = Word(
            **word.model_dump(exclude=["word_link_ids", "word_class_ids"])
        )

        word_to_upsert.word_links = word_links
        word_to_upsert.word_classes = word_classes
        word_to_upsert = await session.merge(word_to_upsert)

        await session.commit()

        output.append(word_to_upsert)
    return output


@router.delete("/{word_id}", status_code=204)
async def delete_word(
    word_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    # first, verify that the user owns this word
    word = (
        await session.scalars(
            select(Word).where(Word.id == word_id).options(joinedload(Word.language))
        )
    ).first()
    if word.language.user_id != current_user.id:
        raise HTTPException(401)

    await session.delete(word)
    await session.commit()
