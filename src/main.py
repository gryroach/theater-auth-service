from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from starlette import status

from api.v1 import api_router as api_v1_router
from core.config import settings
from db import redis
from exceptions.auth_exceptions import AuthError
from exceptions.user_exceptions import UserError


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis.from_url(settings.redis_url)
    try:
        yield
    finally:
        await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description="API сервиса авторизации кинотеатра",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.exception_handler(AuthError)
async def auth_exception_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


@app.exception_handler(UserError)
async def user_exception_handler(request: Request, exc: UserError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
