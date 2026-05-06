import pytest
import requests

pytestmark = pytest.mark.api


class TestUser:

    def test_create_user(self, base_url):
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
        response = requests.post(f"{base_url}/user", json=payload)
        assert response.status_code == 200

    def test_get_user_by_username(self, base_url):
        requests.post(f"{base_url}/user", json={
            "id": 88802, "username": "testuser02", "firstName": "Test",
            "lastName": "User", "email": "test@test.com", "password": "123",
            "phone": "000", "userStatus": 1
        })

        response = requests.get(f"{base_url}/user/testuser02")
        assert response.status_code == 200
        assert response.json()["username"] == "testuser02"

    def test_update_user(self, base_url):
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
        response = requests.put(f"{base_url}/user/testuser03", json=payload)
        assert response.status_code == 200

    def test_delete_user(self, base_url):
        requests.post(f"{base_url}/user", json={
            "id": 88804, "username": "testuser04", "firstName": "Del",
            "lastName": "User", "email": "del@test.com", "password": "123",
            "phone": "000", "userStatus": 1
        })

        response = requests.delete(f"{base_url}/user/testuser04")
        assert response.status_code == 200

    def test_login_user(self, base_url):
        response = requests.get(f"{base_url}/user/login", params={
            "username": "testuser01", "password": "senha123"
        })
        assert response.status_code == 200

    def test_logout_user(self, base_url):
        response = requests.get(f"{base_url}/user/logout")
        assert response.status_code == 200

    def test_get_user_not_found(self, base_url):
        response = requests.get(f"{base_url}/user/nonexistent_user_xyz")
        assert response.status_code == 404
