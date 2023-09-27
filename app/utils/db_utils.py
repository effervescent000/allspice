from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Base, User


async def verify_ownership(
    session: AsyncSession, *, current_user: User, schema: Base, target_ids: list[int]
):
    result = (
        (
            await session.scalars(
                select(schema)
                .where(schema.id.in_(target_ids))
                .options(joinedload(schema.language))
            )
        )
        .unique()
        .all()
    )
    bad_items = [x for x in result if x.language.user_id != current_user.id]
    if len(bad_items) > 0:
        raise HTTPException(401)
