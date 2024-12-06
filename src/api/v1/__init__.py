from fastapi import APIRouter

from .inspection import router as inspect_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(inspect_router, prefix="/inspect", tags=["Inspect"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
