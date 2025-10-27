import pytest
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_register_success(async_client):
    response = async_client.post(
        "/api/auth/register",
        json={
            "email": fake.email(),
            "password": "testpassword123",
            "name": fake.name(),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "name" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client):
    email = fake.email()
    async_client.post(
        "/api/auth/register",
        json={"email": email, "password": "testpassword123", "name": "Test User"},
    )

    response = async_client.post(
        "/api/auth/register",
        json={"email": email, "password": "testpassword123", "name": "Test User"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(async_client):
    email = fake.email()
    password = "testpassword123"
    async_client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "name": "Test User"},
    )

    response = async_client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client):
    response = async_client.post(
        "/api/auth/login",
        json={"email": "nonexistent@test.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

