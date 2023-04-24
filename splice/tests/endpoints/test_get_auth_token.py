import pytest
from rest_framework.test import APIClient

from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestGetAuthToken:
    def setup_method(self, method):
        self.user = create_test_splice_user()
        self.client = APIClient()
        self.url = "/users/get-auth-token/"

    def test_get_user_auth_token(self):
        response = self.client.post(
            path=self.url,
            data={
                "user_id": self.user.username,
                "transaction_id": self.user.get_transaction_id(),
            },
        )

        assert response.status_code == 200
        assert response.json()["Authorization"] is not None

    def test_attempt_authorization_with_wrong_user_id(self):
        response = self.client.post(
            path=self.url,
            data={
                "user_id": "wrong_id",
                "transaction_id": self.user.get_transaction_id(),
            },
        )

        assert response.status_code == 400
        assert "Invalid Auth Credentials" in response.json()["message"]

    def test_attempt_authorization_with_wrong_transaction_id(self):
        user = create_test_splice_user()

        response = self.client.post(
            path=self.url,
            data={"user_id": user.username, "transaction_id": "invalid-transaction-id"},
        )

        assert response.status_code == 400
        assert "Invalid Auth Credentials" in response.json()["message"]
