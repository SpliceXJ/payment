import uuid
import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestCreateSpliceUser:
    client = APIClient()
    url = "/users/create-payment-user/"
    payload = {
        "email": "testuser@gmail.com",
        "user_id": str(uuid.uuid4())[:20]
    }

    def test_create_new_splice_user(self):
        
        response = self.client.post(
            path = self.url,
            data = self.payload
            )

        assert response.status_code == 200
        assert "testuser@gmail.com" in response.json()["data"]["email"]
        assert response.json()["transaction_id"] is not None

        assert SpliceUser.objects.filter(user_id=response.json()["data"]["user_id"]).exists() is True


    def test_create_user_with_existing_email(self):
        test_user_created = create_test_splice_user()

        response = self.client.post(
            path = self.url,
            data = {
                "email": test_user_created.email,
                "user_id": "new_username"
            }
            )

        assert response.status_code == 400
        assert "email already exists" in response.json()["message"]

    
    def test_create_user_with_existing_username(self):
        test_user_created = create_test_splice_user()

        response = self.client.post(
            path = self.url,
            data = {
                "email": "newemail@gmail.com",
                "user_id": test_user_created.username
            }
            )

        assert response.status_code == 400
        assert "username already exists" in response.json()["message"]