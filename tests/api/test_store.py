import pytest
import requests

pytestmark = pytest.mark.api


class TestLoja:

    def test_realizar_pedido(self, base_url):
        payload = {
            "id": 55501,
            "petId": 99901,
            "quantity": 1,
            "shipDate": "2026-05-10T00:00:00.000Z",
            "status": "placed",
            "complete": True
        }
        resposta = requests.post(f"{base_url}/store/order", json=payload)
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["status"] == "placed"
        assert dados["complete"] is True

    def test_buscar_pedido_por_id(self, base_url):
        requests.post(f"{base_url}/store/order", json={
            "id": 55502, "petId": 99901, "quantity": 2,
            "status": "placed", "complete": False
        })

        resposta = requests.get(f"{base_url}/store/order/55502")
        assert resposta.status_code == 200
        assert resposta.json()["quantity"] == 2

    def test_deletar_pedido(self, base_url):
        requests.post(f"{base_url}/store/order", json={
            "id": 55503, "petId": 99901, "quantity": 1,
            "status": "placed", "complete": False
        })

        resposta = requests.delete(f"{base_url}/store/order/55503")
        assert resposta.status_code == 200

    def test_obter_inventario(self, base_url):
        resposta = requests.get(f"{base_url}/store/inventory")
        assert resposta.status_code == 200
        dados = resposta.json()
        assert isinstance(dados, dict)
        assert len(dados) > 0

    def test_pedido_nao_encontrado(self, base_url):
        resposta = requests.get(f"{base_url}/store/order/0")
        assert resposta.status_code == 404
