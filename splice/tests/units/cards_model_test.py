import uuid
import pytest
import random
from faker import Faker

from splice.users.models.user import SpliceUser
from splice.users.models.cards import UsersCard
from splice.tests.test_helpers.create_test_user import create_test_splice_user
from splice.tests.test_helpers.create_test_card import create_test_card


@pytest.mark.django_db
def test_user_create_card():
    user: SpliceUser = create_test_splice_user()
    assert SpliceUser.objects.filter(id=user.id).exists()

    UsersCard.create(
        owner=user,
        authorization=str(uuid.uuid4())[:25],
        email=Faker().email,
        last_four_digits=random.randint(1000, 9999),
        card_type=random.choice(["Visa", "Master", "Verve"]),
    )

    assert UsersCard.objects.filter(owner=user).exists()

    for _ in range(15):
        test_user = create_test_splice_user()
        assert SpliceUser.objects.filter(id=test_user.id).exists()

        # create 3 cards for each user
        for _ in range(3):
            create_test_card(owner=test_user)
        assert UsersCard.objects.filter(owner=test_user).count() == 3

    # assert all cards were created
    assert UsersCard.objects.all().count() == (15 * 3) + 1


@pytest.mark.django_db
def test_user_deleted_and_card_deleted():
    test_user = create_test_splice_user()
    assert SpliceUser.objects.filter(id=test_user.id).exists()

    create_test_card(owner=test_user)
    assert UsersCard.objects.filter(owner=test_user).count() == 1

    test_user.delete()

    assert SpliceUser.objects.filter(id=test_user.id).exists() is False
    assert UsersCard.objects.filter(owner=test_user).count() == 0
