import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "acc_data",
    (
        (1, "Address on this network already exists."),
        (2, "Account does not exist."),
    ),
)
async def test_address_create_fails(client: AsyncClient, token: str, acc_data):
    acc_id, error = acc_data
    response = await client.post(
        "/address/create",
        headers={"Authorization": f"Bearer {token}"},
        params={"account_id": acc_id, "network": "BTC"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == error


@pytest.mark.asyncio
async def test_address_create_succeeds(client: AsyncClient, token: str):
    response = await client.post(
        "/address/create",
        headers={"Authorization": f"Bearer {token}"},
        params={"account_id": 1, "network": "ETH"},
    )
    assert response.status_code == 200
    assert sorted(tuple(response.json().keys())) == ["address", "id", "network"]


@pytest.mark.asyncio
@pytest.mark.parametrize("acc_data", ((1, True), (2, False)))
async def test_address_list(client: AsyncClient, token: str, acc_data):
    acc_id, acc_exists = acc_data
    response = await client.get(
        "/address/list",
        headers={"Authorization": f"Bearer {token}"},
        params={"account_id": acc_id},
    )

    if acc_exists:
        assert len(response.json()) == 1
    else:
        assert response.status_code == 400
        assert response.json()["detail"] == "Account does not exist."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "acc_data", ((1, 1, True, True), (1, 2, True, False), (2, 2, False, False))
)
async def test_address_retrieve(client: AsyncClient, token: str, acc_data):
    acc_id, addr_id, acc_exists, addr_exists = acc_data
    response = await client.get(
        "/address/retrieve",
        headers={"Authorization": f"Bearer {token}"},
        params={"account_id": acc_id, "address_id": addr_id},
    )
    if acc_exists:
        assert (response.json() is not None) == addr_exists
    else:
        assert response.status_code == 400
        assert response.json()["detail"] == "Account does not exist."
