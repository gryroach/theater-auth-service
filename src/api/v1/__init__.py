from fastapi import APIRouter

from .auth import router as auth_router
from .inspection import router as inspect_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(inspect_router, prefix="/inspect", tags=["Inspect"])
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
