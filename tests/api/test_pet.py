import pytest
import requests

pytestmark = pytest.mark.api


class TestPet:

    def test_adicionar_pet(self, base_url):
        payload = {
            "id": 99901,
            "name": "Rex",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/rex.jpg"],
            "tags": [{"id": 1, "name": "trained"}],
            "status": "available"
        }
        resposta = requests.post(f"{base_url}/pet", json=payload)
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["name"] == "Rex"
        assert dados["status"] == "available"

    def test_buscar_pet_por_id(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99902, "name": "Buddy", "photoUrls": ["url"], "status": "available"
        })

        resposta = requests.get(f"{base_url}/pet/99902")
        assert resposta.status_code == 200
        assert resposta.json()["name"] == "Buddy"

    def test_atualizar_pet(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99903, "name": "Max", "photoUrls": ["url"], "status": "available"
        })

        payload = {
            "id": 99903,
            "name": "Max Updated",
            "photoUrls": ["url"],
            "status": "sold"
        }
        resposta = requests.put(f"{base_url}/pet", json=payload)
        assert resposta.status_code == 200
        assert resposta.json()["name"] == "Max Updated"
        assert resposta.json()["status"] == "sold"

    def test_buscar_pet_por_status(self, base_url):
        resposta = requests.get(f"{base_url}/pet/findByStatus", params={"status": "available"})
        assert resposta.status_code == 200
        pets = resposta.json()
        assert isinstance(pets, list)
        assert len(pets) > 0

    def test_deletar_pet(self, base_url):
        requests.post(f"{base_url}/pet", json={
            "id": 99904, "name": "ToDelete", "photoUrls": ["url"], "status": "available"
        })

        resposta = requests.delete(f"{base_url}/pet/99904")
        assert resposta.status_code == 200

    def test_pet_nao_encontrado(self, base_url):
        resposta = requests.get(f"{base_url}/pet/0")
        assert resposta.status_code == 404
