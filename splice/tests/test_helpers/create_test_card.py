import uuid
import random
from faker import Faker

from splice.users.models.cards import UsersCard
from splice.tests.test_helpers.create_test_user import create_test_splice_user


def create_test_card(owner=None) -> "UsersCard":
    return UsersCard.create(
        owner=owner or create_test_splice_user(),
        authorization=str(uuid.uuid4())[:25],
        email=Faker().email(),
        last_four_digits=random.randrange(1000, 9999),
        card_type=random.choice(["visa", "master", "verve"]),
    )
