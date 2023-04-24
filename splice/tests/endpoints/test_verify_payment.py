import os
from dotenv import load_dotenv
load_dotenv()

import pytest
from copy import copy
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_payment import create_test_payment
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestVerifyPayment:

    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)
        self.recepient: SpliceUser = create_test_splice_user()

        self.payment_instance: Payments = create_test_payment(initiator=self.user)
        
        self.url = "/payments/verify-payment/"
        self.payload = {
            "reference": os.getenv("TEST_PAYMENT_REF"),
            "save_card": True,
            "payment_instance_id": self.payment_instance.id  
        }
           

    def test_verify_payment_instance_with_invalid_reference(self):
        # alter the payload and change the reference
        altered_payload = copy(self.payload)
        altered_payload["reference"] = "invalid-reference"

        response = self.client.post(
            path = self.url,
            data = altered_payload
            )

        assert response.status_code == 400
        assert "transaction not successful" in response.json()["message"]

    
    def test_verify_payment_instance_with_valid_reference(self):
        """ this test must not be ran outside local enviroment """

        if os.getenv("ENVIROMENT") == "LOCAL":
            response = self.client.post(
                path = self.url,
                data = self.payload
                )

            assert response.status_code == 200
            assert "successful" in response.json()["message"]    
