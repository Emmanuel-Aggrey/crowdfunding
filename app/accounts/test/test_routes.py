from app.test.base import BaseTest
from fastapi import status

from app.accounts.factories import UserFactory


class TestAccount(BaseTest):

    def test_create_user(self):

        response = self.client.post(
            "/accounts/register/",
            json={
                "username": "deadpool",
                "email": "deadpool@example.com",
                "password": "chimichangas4life",
            },
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["email"] == "deadpool@example.com"
        assert "id" in data

    def test_gimme_jwt(self):
        json = {"email": "deadpool@example.com",
                "password": "chimichangas4life"}
        response = self.client.post("/accounts/login/", json=json)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_get_user(self):
        user = UserFactory()

        self.force_authenticate(user)
        response = self.client.get("/accounts/me/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == user.email
