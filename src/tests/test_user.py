from uuid import UUID

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import User
from services.roles import Roles


@pytest_asyncio.fixture
async def create_user(session: AsyncSession) -> User:
    """Создание пользователя"""
    user = User(
        login="testuser",
        role=Roles.admin.name,
        password="123",
        first_name="Tester",
        last_name="Pass",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_user_role(client: AsyncClient, create_user: User) -> None:
    """
    Тест для получения роли пользователя
    """
    response = await client.get(f"api/v1/users/{create_user.id}/role")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == Roles.admin.name
    assert data["permissions"] == Roles.admin.permissions.model_dump()


@pytest.mark.asyncio
async def test_set_user_role(client: AsyncClient, create_user: User) -> None:
    """
    Тест для обновления роли пользователя
    """
    new_role = {"role": "moderator"}
    response = await client.patch(
        f"api/v1/users/{create_user.id}/role",
        json=new_role,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "moderator"
    assert data["permissions"] == Roles.moderator.permissions.model_dump()


@pytest.mark.asyncio
async def test_get_user_role_not_found(client: AsyncClient) -> None:
    """
    Тест для проверки ошибки при получении роли несуществующего пользователя
    """
    non_existent_user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    response = await client.get(f"api/v1/users/{non_existent_user_id}/role")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User does not exists"


@pytest.mark.asyncio
async def test_set_user_role_not_found(client: AsyncClient) -> None:
    """
    Тест для проверки ошибки при обновлении роли несуществующего пользователя
    """
    non_existent_user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    new_role = {"role": "moderator"}
    response = await client.patch(
        f"api/v1/users/{non_existent_user_id}/role",
        json=new_role,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User does not exists"


@pytest.mark.asyncio
async def test_set_user_role_invalid(
        client: AsyncClient, create_user: User
) -> None:
    """
    Тест для проверки ошибки при обновлении роли на несуществующую роль
    """
    invalid_role = {"role": "invalid_role"}
    response = await client.patch(
        f"api/v1/users/{create_user.id}/role", json=invalid_role
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["msg"] == "Value error, Role does not exists"
