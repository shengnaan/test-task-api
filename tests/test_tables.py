
import pytest


@pytest.mark.asyncio
async def test_table_crud(client, override_get_db) -> None:
    response = await client.post("/api/v1/tables/", json={
        "name": "Test Table",
        "seats": 4,
        "location": "Зал у окна"
    })
    assert response.status_code == 201
    table = response.json()
    assert table["name"] == "Test Table"

    table_id = table["id"]

    response = await client.get("/api/v1/tables/")
    assert response.status_code == 200
    assert any(t["id"] == table_id for t in response.json())

    response = await client.delete(f"/api/v1/tables/{table_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_nonexistent_table(client, override_get_db) -> None:
    response = await client.delete("/api/v1/tables/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Столик не найден."


@pytest.mark.asyncio
async def test_create_table_invalid_data(client, override_get_db) -> None:
    response = await client.post("/api/v1/tables/", json={
        "name": "",
        "seats": 4,
        "location": "Зал"
    })
    assert response.status_code == 201

    response = await client.post("/api/v1/tables/", json={
        "name": "Table",
        "seats": 0,
        "location": "Терраса"
    })
    assert response.status_code == 422

    response = await client.post("/api/v1/tables/", json={
        "name": "Table",
        "seats": 4
    })
    assert response.status_code == 422
