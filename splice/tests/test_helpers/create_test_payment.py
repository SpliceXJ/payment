import uuid
import pytest
import random
from faker import Faker

from splice.users.models.user import SpliceUser
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
def create_test_payment(
    amount=None, initiator=None, recepient=None, reference=None
) -> "Payments":
    return Payments.create(
        amount=amount or random.randint(10, 5000),
        initiator=initiator or create_test_splice_user(),
        recepient=recepient or create_test_splice_user(),
        item_id=str(uuid.uuid4())[:15],
        reference=reference,
    )
