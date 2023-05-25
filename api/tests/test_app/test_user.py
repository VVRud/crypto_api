import pytest
from httpx import AsyncClient
from jose import jwt
from models import User
from modules.auth import Auth


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    (
        (
            {"username": "user", "password": "less8"},
            422,
            "ensure this value has at least 8 characters",
        ),
        (
            {"username": "uname", "password": "password_long"},
            400,
            "Username already exists.",
        ),
    ),
)
async def test_users_create_fails(client: AsyncClient, data):
    json, code, msg = data
    response = await client.post("/user/create", json=json)
    assert response.status_code == code
    assert msg in response.content.decode("utf-8")


@pytest.mark.asyncio
async def test_users_create_succeeds(client: AsyncClient, user: User):
    response = await client.post(
        "/user/create",
        json={"username": user.username + "1", "password": user.password},
    )
    assert response.status_code == 200
    assert sorted(tuple(response.json().keys())) == ["id", "username"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    (
        {"username": "user", "password": "less8"},
        {"username": "uname", "password": "password_long"},
    ),
)
async def test_jwt_create_fails(client: AsyncClient, data):
    response = await client.post("/user/token", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_jwt_create_succeeds(client: AsyncClient, user: User, auth: Auth):
    response = await client.post(
        "/user/token", data={"username": user.username, "password": "12345678"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["token_type"] == "bearer"
    user_jwt = jwt.decode(
        response_data["access_token"],
        auth.jwt_secret_token,
        algorithms=[auth.JWT_ALGORITHM],
    )["sub"]
    assert user_jwt == user.username


@pytest.mark.asyncio
async def test_jwt_expired(client: AsyncClient, user: User, auth: Auth):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1bmFtZSIsImV4cCI6MTY4NTAyMjkwN30.oZlYh6HiYoEOtvSjTp3E1k1F_Hs2Jt0XvouTg2VS1Lw"
    response = await client.post(
        "/account/create", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials."
