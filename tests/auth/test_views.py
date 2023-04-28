import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    user_data = {"email": "testuser@example.com", "name": "Test User"}
    response = await client.post("/api/auth/users", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == user_data["email"]
    assert user["name"] == user_data["name"]
    assert "id" in user


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient) -> None:
    response = await client.get("/api/auth/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
