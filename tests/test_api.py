"""
API tests. These call the real endpoints and need a running Postgres database.
In GitHub Actions, the workflow starts Postgres for us as a "service container".
"""

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_save_and_list_supplier():
    with TestClient(app) as client:
        # Save a messy record
        response = client.post(
            "/suppliers",
            json={"name": "  nova  thrusters ", "email": "HI@NOVA.com", "price": "$5,000", "date": "03/15/2026"},
        )
        assert response.status_code == 200
        saved = response.json()
        assert saved["name"] == "Nova Thrusters"

        # Make sure the cleaned record is in the database
        all_suppliers = client.get("/suppliers").json()
        assert any(s["id"] == saved["id"] and s["price"] == 5000.0 for s in all_suppliers)
