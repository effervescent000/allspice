from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Language, User
from app.schemas.requests import LanguageRequest
from app.schemas.responses import LanguageResponse

router = APIRouter()


@router.post("/", response_model=LanguageResponse)
async def upsert_language(
    languages: list[LanguageRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Upsert a language. For consistency's sake, we expect a list here,
    but we only accept the first item of it."""
    new_language = languages[0]
    language = Language(**new_language.model_dump(), user_id=current_user.id)
    session.add(language)
    await session.commit()
    return language
