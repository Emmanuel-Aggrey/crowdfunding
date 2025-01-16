from app.test.base import BaseTest
from fastapi import status
from app.accounts.factories import UserFactory
from faker import Faker

fake = Faker()


class TestAccount(BaseTest):
    random_email = fake.email()
    password = "testuser@33"

    @classmethod
    def get_random_email(cls):
        return cls.random_email

    @classmethod
    def get_password(cls):
        return cls.password

    def test_create_user(self):
        # Use the class-level random email
        random_email = self.get_random_email()

        # Register the user with the randomly generated email
        response = self.client.post(
            "/accounts/register/",
            json={
                "username": "testuser",
                "email": random_email,
                "password": self.get_password(),
            },
        )

        # Assert that the registration is successful
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()

        assert data["email"] == random_email
        assert "id" in data

    def test_gimme_jwt(self):
        # Use the same random email for login
        random_email = self.get_random_email()
        password = self.get_password()

        # Register the user first
        self.client.post(
            "/accounts/register/",
            json={
                "username": "testuser",
                "email": random_email,
                "password": password,
            },
        )

        # Log in with the same credentials
        json = {"email": random_email, "password": password}
        response = self.client.post("/accounts/login/", json=json)

        # Assert that the login was successful and a JWT is returned
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
