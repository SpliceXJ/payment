import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestUpdateSpliceUser:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = "/users/update-payment-user/"
        self.payload = {"email": "testuserupdated@gmail.com", "is_vendor": True}

    def test_update_splice_user_email_and_vendor(self):
        assert self.user.is_vendor is False

        response = self.client.put(path=self.url, data=self.payload)

        assert response.status_code == 200
        assert "testuserupdated@gmail.com" in response.json()["data"]["email"]

        assert SpliceUser.objects.get(id=self.user.id).is_vendor is True
        assert (
            SpliceUser.objects.get(id=self.user.id).email == "testuserupdated@gmail.com"
        )

    def test_update_splice_user_with_existing_email(self):
        test_user_created = create_test_splice_user()

        response = self.client.put(
            path=self.url, data={"email": test_user_created.email}
        )

        assert response.status_code == 400
        assert "email already exists" in response.json()["message"]
