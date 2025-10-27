import pytest
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_create_user(async_client):
    response = async_client.post(
        "/api/users/",
        json={"email": fake.email(), "password": "testpassword123", "name": fake.name()},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "email" in data


@pytest.mark.asyncio
async def test_get_users(async_client):
    email1 = fake.email()
    email2 = fake.email()

    async_client.post(
        "/api/users/",
        json={"email": email1, "password": "testpassword123", "name": "User 1"},
    )
    async_client.post(
        "/api/users/",
        json={"email": email2, "password": "testpassword123", "name": "User 2"},
    )

    response = async_client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) >= 2


@pytest.mark.asyncio
async def test_get_user_by_id(async_client):
    response = async_client.post(
        "/api/users/",
        json={"email": fake.email(), "password": "testpassword123", "name": "Test User"},
    )
    user_id = response.json()["id"]

    response = async_client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found(async_client):
    response = async_client.get("/api/users/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

