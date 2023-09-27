from fastapi import APIRouter

from app.api.endpoints import auth, languages, phonology, sc, users, word_links, words

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])
api_router.include_router(word_links.router, prefix="/word_links", tags=["word_links"])
api_router.include_router(words.router, prefix="/words", tags=["words"])
api_router.include_router(phonology.router, prefix="/phonology", tags=["phonology"])
api_router.include_router(sc.router, prefix="/sc", tags=["sound_change"])
