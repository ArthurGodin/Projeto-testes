import pytest
import requests

pytestmark = pytest.mark.api


class TestPet:

    def test_add_pet(self, base_url):
        payload = {
            "id": 99901,
            "name": "Rex",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/rex.jpg"],
            "tags": [{"id": 1, "name": "trained"}],
            "status": "available"
        }
        response = requests.post(f"{base_url}/pet", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Rex"
        assert data["status"] == "available"

    def test_get_pet_by_id(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99902, "name": "Buddy", "photoUrls": ["url"], "status": "available"
        })

        response = requests.get(f"{base_url}/pet/99902")
        assert response.status_code == 200
        assert response.json()["name"] == "Buddy"

    def test_update_pet(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99903, "name": "Max", "photoUrls": ["url"], "status": "available"
        })

        payload = {
            "id": 99903,
            "name": "Max Updated",
            "photoUrls": ["url"],
            "status": "sold"
        }
        response = requests.put(f"{base_url}/pet", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Max Updated"
        assert response.json()["status"] == "sold"

    def test_find_pet_by_status(self, base_url):
        response = requests.get(f"{base_url}/pet/findByStatus", params={"status": "available"})
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert len(pets) > 0

    def test_delete_pet(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99904, "name": "ToDelete", "photoUrls": ["url"], "status": "available"
        })

        response = requests.delete(f"{base_url}/pet/99904")
        assert response.status_code == 200

    def test_get_pet_not_found(self, base_url):
        response = requests.get(f"{base_url}/pet/0")
        assert response.status_code == 404
