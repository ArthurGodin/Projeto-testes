import pytest
import requests

pytestmark = pytest.mark.api


class TestUsuario:

    def test_criar_usuario(self, base_url):
        payload = {
            "id": 88801,
            "username": "testuser01",
            "firstName": "Arthur",
            "lastName": "Godinho",
            "email": "arthur@test.com",
            "password": "senha123",
            "phone": "11999999999",
            "userStatus": 1
        }
        resposta = requests.post(f"{base_url}/user", json=payload)
        assert resposta.status_code == 200

    def test_buscar_usuario_por_username(self, base_url):
        requests.post(f"{base_url}/user", json={
            "id": 88802, "username": "testuser02", "firstName": "Test",
            "lastName": "User", "email": "test@test.com", "password": "123",
            "phone": "000", "userStatus": 1
        })

        resposta = requests.get(f"{base_url}/user/testuser02")
        assert resposta.status_code == 200
        assert resposta.json()["username"] == "testuser02"

    def test_atualizar_usuario(self, base_url):
        requests.post(f"{base_url}/user", json={
            "id": 88803, "username": "testuser03", "firstName": "Old",
            "lastName": "Name", "email": "old@test.com", "password": "123",
            "phone": "000", "userStatus": 1
        })

        payload = {
            "id": 88803, "username": "testuser03", "firstName": "New",
            "lastName": "Name", "email": "new@test.com", "password": "456",
            "phone": "111", "userStatus": 1
        }
        resposta = requests.put(f"{base_url}/user/testuser03", json=payload)
        assert resposta.status_code == 200

    def test_deletar_usuario(self, base_url):
        requests.post(f"{base_url}/user", json={
            "id": 88804, "username": "testuser04", "firstName": "Del",
            "lastName": "User", "email": "del@test.com", "password": "123",
            "phone": "000", "userStatus": 1
        })

        resposta = requests.delete(f"{base_url}/user/testuser04")
        assert resposta.status_code == 200

    def test_login_usuario(self, base_url):
        resposta = requests.get(f"{base_url}/user/login", params={
            "username": "testuser01", "password": "senha123"
        })
        assert resposta.status_code == 200

    def test_logout_usuario(self, base_url):
        resposta = requests.get(f"{base_url}/user/logout")
        assert resposta.status_code == 200

    def test_usuario_nao_encontrado(self, base_url):
        resposta = requests.get(f"{base_url}/user/nonexistent_user_xyz")
        assert resposta.status_code == 404
