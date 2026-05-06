import pytest
import requests

pytestmark = pytest.mark.api


class TestStore:

    def test_place_order(self, base_url):
        payload = {
            "id": 55501,
            "petId": 99901,
            "quantity": 1,
            "shipDate": "2026-05-10T00:00:00.000Z",
            "status": "placed",
            "complete": True
        }
        response = requests.post(f"{base_url}/store/order", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "placed"
        assert data["complete"] is True

    def test_get_order_by_id(self, base_url):
        requests.post(f"{base_url}/store/order", json={
            "id": 55502, "petId": 99901, "quantity": 2,
            "status": "placed", "complete": False
        })

        response = requests.get(f"{base_url}/store/order/55502")
        assert response.status_code == 200
        assert response.json()["quantity"] == 2

    def test_delete_order(self, base_url):
        requests.post(f"{base_url}/store/order", json={
            "id": 55503, "petId": 99901, "quantity": 1,
            "status": "placed", "complete": False
        })

        response = requests.delete(f"{base_url}/store/order/55503")
        assert response.status_code == 200

    def test_get_inventory(self, base_url):
        response = requests.get(f"{base_url}/store/inventory")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_get_order_not_found(self, base_url):
        response = requests.get(f"{base_url}/store/order/0")
        assert response.status_code == 404
