from datetime import UTC, datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_reservation_crud_and_conflict(client, override_get_db) -> None:
    table_resp = await client.post("/api/v1/tables/", json={
        "name": "Table",
        "seats": 2,
        "location": "Терраса"
    })
    table_id = table_resp.json()["id"]

    reservation_time = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=1)
    payload = {
        "customer_name": "Иван",
        "table_id": table_id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 45
    }

    r = await client.post("/api/v1/reservations/", json=payload)
    assert r.status_code == 201
    reservation_id = r.json()["id"]

    r_conflict = await client.post("/api/v1/reservations/", json=payload)
    assert r_conflict.status_code == 400

    all_r = await client.get("/api/v1/reservations/")
    assert all_r.status_code == 200
    assert any(r["id"] == reservation_id for r in all_r.json())

    r_del = await client.delete(f"/api/v1/reservations/{reservation_id}")
    assert r_del.status_code == 204

    await client.delete(f"/api/v1/tables/{table_id}")


@pytest.mark.asyncio
async def test_create_reservation_with_invalid_duration(client, override_get_db) -> None:
    table_resp = await client.post("/api/v1/tables/", json={
        "name": "RTest",
        "seats": 2,
        "location": "Зал"
    })
    table_id = table_resp.json()["id"]

    payload = {
        "customer_name": "Too Short",
        "table_id": table_id,
        "reservation_time": (datetime.now(UTC).replace(tzinfo=None)+ timedelta(minutes=1)).isoformat(),
        "duration_minutes": 15
    }
    response = await client.post("/api/v1/reservations/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_reservation_on_invalid_table(client, override_get_db) -> None:
    payload = {
        "customer_name": "Ghost",
        "table_id": 9999,
        "reservation_time": (datetime.now(UTC).replace(tzinfo=None)+ timedelta(minutes=1)).isoformat(),
        "duration_minutes": 45
    }
    response = await client.post("/api/v1/reservations/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Столика с таким ID нет."


@pytest.mark.asyncio
async def test_create_reservation_in_past(client, override_get_db) -> None:
    table_resp = await client.post("/api/v1/tables/", json={
        "name": "Past",
        "seats": 2,
        "location": "Терраса"
    })
    table_id = table_resp.json()["id"]

    payload = {
        "customer_name": "Назад во времени",
        "table_id": table_id,
        "reservation_time": (datetime.now(UTC).replace(tzinfo=None) - timedelta(hours=1)).isoformat(),
        "duration_minutes": 45
    }
    response = await client.post("/api/v1/reservations/", json=payload)
    print(response.status_code)

    await client.delete(f"/api/v1/tables/{table_id}")
