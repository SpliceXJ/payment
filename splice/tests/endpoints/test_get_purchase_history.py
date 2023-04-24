import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_payment import create_test_payment
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestGetPurchaseHistory:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = "/payments/get-purchase-history/"

    def test_get_purchase_history(self):
        # create 20 completed purchases for user
        for _ in range(20):
            instance = create_test_payment(initiator=self.user)
            instance.is_completed = True
            instance.save()

        # verify all instances were created
        assert Payments.objects.filter(initiator=self.user).count() == 20

        response = self.client.get(path=self.url)

        assert response.status_code == 200
        assert len(response.json()["data"]) == 20

    def test_get_purchase_history_with_some_incomplete_purchases(self):
        # create 10 completed purchases for user
        for _ in range(10):
            instance = create_test_payment(initiator=self.user)
            instance.is_completed = True
            instance.save()

        # create 5 completed purchases for user
        for _ in range(5):
            instance = create_test_payment(initiator=self.user)
            instance.is_completed = True
            instance.save()

        # verify all instances were created
        assert Payments.objects.filter(initiator=self.user).count() == 15

        response = self.client.get(path=self.url)

        assert response.status_code == 200
        assert len(response.json()["data"]) == 15
