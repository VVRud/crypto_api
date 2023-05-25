import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_account_create_fails(client: AsyncClient, token: str):
    response = await client.post(
        "/account/create",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": "acc_name"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Account with this name already exists."


@pytest.mark.asyncio
async def test_account_create_succeeds(client: AsyncClient, token: str):
    response = await client.post(
        "/account/create",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": "acc_new_name"},
    )
    assert response.status_code == 200
    assert sorted(tuple(response.json().keys())) == ["id", "name"]


@pytest.mark.asyncio
async def test_account_list(client: AsyncClient, token: str):
    response = await client.get(
        "/account/list", headers={"Authorization": f"Bearer {token}"}
    )

    assert len(response.json()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("acc_data", ((1, True), (2, False)))
async def test_account_list(client: AsyncClient, token: str, acc_data):
    acc_id, acc_exists = acc_data
    response = await client.get(
        "/account/retrieve",
        headers={"Authorization": f"Bearer {token}"},
        params={"account_id": acc_id},
    )
    assert (response.json() is not None) == acc_exists
