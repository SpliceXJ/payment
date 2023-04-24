import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestGetTransactionId:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = "/users/get-transaction-id/"

    def test_get_user_transaction_id(self):
        response = self.client.get(path=self.url)

        assert response.status_code == 200
        assert response.json()["transaction_id"] == self.user.get_transaction_id()
