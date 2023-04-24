import os
from dotenv import load_dotenv

load_dotenv()

import pytest
from copy import copy
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.users.models.cards import UsersCard
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_payment import create_test_payment
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestMakePaymentUsingSavedCard:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.recepient: SpliceUser = create_test_splice_user()

        self.payment_instance: Payments = create_test_payment(initiator=self.user)

        self.url = "/payments/pay-using-saved-card/"

        self.verify_payment_payload = {
            "reference": os.getenv("TEST_PAYMENT_REF"),
            "save_card": True,
            "payment_instance_id": self.payment_instance.id,
        }

    """ 
        Here's the flow; user makes a complete transaction at least once,
        If successful, card is saved is saved for future transactions
        1. we verify successful transaction
        2. we use the card to initiate subsequent transaction
    """

    def test_pay_using_my_card(self):
        """this test must not be ran outside local enviroment"""

        if os.getenv("ENVIROMENT") == "LOCAL":
            # first step: create transaction and pay, card get stored
            verify_trans_response = self.client.post(
                path="/payments/verify-payment/", data=self.verify_payment_payload
            )

            assert verify_trans_response.status_code == 200
            assert "successful" in verify_trans_response.json()["message"]

            # second step: used saved card to complete another transaction
            new_payment_instance = create_test_payment(initiator=self.user)

            card = UsersCard.objects.filter(owner=self.user).first()

            payload = {
                "payment_instance_id": new_payment_instance.id,
                "card_id": card.id,
            }

            response = self.client.post(path=self.url, data=payload)

            assert response.status_code == 200
            assert "successful" in response.json()["message"]
