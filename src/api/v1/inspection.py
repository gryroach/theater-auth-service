import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from asyncpg.exceptions import PostgresError
from redis import (
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)

from db.postgres import get_session
from db.redis import get_redis
from schemas.inspect import Ping, DatabaseStatus, Status, RedisStatus

router = APIRouter()


@router.get(
    "/ping",
    response_model=Ping,
    description="Get connection time to services and get info.",
)
async def ping_services(
    db: AsyncSession = Depends(get_session),
    redis: AsyncSession = Depends(get_redis),
) -> Ping:
    """
    Ping services
    """
    db_connected = True
    db_info = ""
    db_time = 0

    # ping database
    try:
        bd_start = time.time()
        ping = await db.execute(text("SELECT version()"))
        db_time = time.time() - bd_start
        db_info = ping.scalar_one_or_none()
    except (PostgresError, ConnectionRefusedError, TimeoutError):
        db_connected = False

    redis_connected = True
    redis_info = ""
    redis_time = 0

    # ping redis
    try:
        redis_start = time.time()
        ping = await redis.ping()
        redis_time = time.time() - redis_start
        redis_info = "PONG" if ping else "NO PONG"
    except (RedisConnectionError, RedisTimeoutError):
        redis_connected = False

    return Ping(
        database=DatabaseStatus(
            status=(
                Status.connected.value
                if db_connected
                else Status.error.value
            ),
            info=db_info,
            time=db_time,
        ),
        redis=RedisStatus(
            status=(
                Status.connected.value
                if redis_connected
                else Status.error.value
            ),
            info=redis_info,
            time=redis_time,
        ),
    )
