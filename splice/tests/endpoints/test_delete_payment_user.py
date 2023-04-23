import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestUpdateSpliceUser:

    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

        self.url = "/users/delete-payment-user/"
        

    def test_delete_splice_user(self):
        assert SpliceUser.objects.filter(id=self.user.id).exists() is True

        response = self.client.post(path = self.url)

        assert response.status_code == 200
        assert "deleted" in response.json()["message"]

        assert SpliceUser.objects.filter(id=self.user.id).exists() is False
