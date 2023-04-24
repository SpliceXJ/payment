import uuid
import pytest
from copy import copy
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_payment import create_test_payment
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestCreatePaymentInstance:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.recepient: SpliceUser = create_test_splice_user()

        self.url = "/payments/create-payment-instance/"
        self.payload = {
            "recepient_id": self.recepient.username,
            "recepient_transaction_id": self.recepient.get_transaction_id(),
            "amount": 1000,
            "item_id": str(uuid.uuid4())[:20],
        }

    def test_create_payment_instance_with_invalid_recepient_id(self):
        # alter the payload and change the recepient id
        altered_payload = copy(self.payload)
        altered_payload["recepient_id"] = "wrong-recepient-id"

        response = self.client.post(path=self.url, data=altered_payload)

        assert response.status_code == 401
        assert "recepient does not exist" in response.json()["message"]

    def test_create_payment_instance_with_invalid_recepient_transaction_id(self):
        # alter the payload and change the recepient id
        altered_payload = copy(self.payload)
        altered_payload["recepient_transaction_id"] = "wrong-recepient-transaction-id"

        response = self.client.post(path=self.url, data=altered_payload)

        assert response.status_code == 400
        assert "recepient transaction id invalid" in response.json()["message"]

    def test_create_payment_instance(self):
        response = self.client.post(path=self.url, data=self.payload)

        assert response.status_code == 200
        assert response.json()["recepient"]["user_id"] == str(self.recepient.user_id)
        assert response.json()["initiator"]["user_id"] == str(self.user.user_id)
        assert response.json()["amount"] == self.payload["amount"]
        assert response.json()["item_id"] == self.payload["item_id"]

        assert (
            Payments.objects.filter(
                recepient=self.recepient,
                initiator=self.user,
                amount=self.payload["amount"],
                item_id=self.payload["item_id"],
            ).exists()
            is True
        )
