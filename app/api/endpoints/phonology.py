from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api import deps
from app.models import Language, Phone, User
from app.schemas.requests import PhonologyRequest
from app.schemas.responses import PhoneResponse
from app.utils.db_utils import verify_ownership

router = APIRouter()


@router.post("/", response_model=list[PhoneResponse])
async def upsert_phones(
    phonology: list[PhonologyRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Again, we're just popping off the first item in the list but accepting
    a list for consistency's sake.
    """
    phones = phonology[0].phonology
    mode = phonology[0].mode
    await verify_ownership(
        session,
        current_user=current_user,
        schema=Phone,
        target_ids=[x.id for x in phones],
    )

    if mode == "insert":
        output = []
        for phone in phones:
            new_phone = Phone(**phone.model_dump())
            upserted = await session.merge(new_phone)
            output.append(upserted)
        await session.commit()
        return output
    if mode == "replace":
        language = (
            (
                await session.scalars(
                    select(Language)
                    .where(Language.id == phones[0].language_id)
                    .options(joinedload(Language.phones))
                )
            )
            .unique()
            .first()
        )
        models = []
        for phone in phones:
            model = await session.merge(Phone(**phone.model_dump()))
            models.append(model)
        language.phones = models
        await session.commit()
        return models


@router.get("/by_language/{language_id}", response_model=list[PhoneResponse])
async def get_language_phones(
    language_id: int,
    # current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    phones = (
        await session.scalars(select(Phone).where(Phone.language_id == language_id))
    ).all()
    return phones


@router.delete("/{phone_id}", status_code=204)
async def delete_phone(
    phone_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    await verify_ownership(
        session, current_user=current_user, schema=Phone, target_ids=[phone_id]
    )
    await session.execute(delete(Phone).where(Phone.id == phone_id))
    await session.commit()
