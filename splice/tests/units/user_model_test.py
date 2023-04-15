import uuid
import pytest
from faker import Faker

from splice.users.models.user import SpliceUser


@pytest.mark.django_db
def test_create_user() -> None:
    new_user: SpliceUser = SpliceUser.create(
        email=Faker().email, username=str(uuid.uuid4())[:15]
    )
    assert new_user.transaction_id is not None and uuid.UUID(
        new_user.get_transaction_id()
    )
    assert SpliceUser.objects.all().count() == 1
    assert SpliceUser.objects.filter(user_id=new_user.user_id).exists()


@pytest.mark.django_db
def test_create_users() -> None:
    for num in range(40):
        created_user: SpliceUser = SpliceUser.create(
            email=Faker().email, username=str(uuid.uuid4())[:15]
        )
        assert created_user.transaction_id is not None
        assert SpliceUser.objects.all().count() == num + 1  # nums starts from 0
        assert SpliceUser.objects.filter(user_id=created_user.user_id).exists()

    assert SpliceUser.objects.all().count() == 40


@pytest.mark.django_db
def test_update_user() -> None:
    for _ in range(10):
        created_user: SpliceUser = SpliceUser.create(
            email=Faker().email, username=str(uuid.uuid4())[:15]
        )
        assert created_user.is_vendor is False
        # update is vendor
        created_user.is_vendor = True
        created_user.save()
        assert created_user.is_vendor is True


@pytest.mark.django_db
def test_delete_user() -> None:
    new_user: SpliceUser = SpliceUser.create(
        email=Faker().email, username=str(uuid.uuid4())[:15]
    )
    assert SpliceUser.objects.all().count() == 1
    assert SpliceUser.objects.filter(user_id=new_user.user_id).exists()

    new_user.delete()

    assert SpliceUser.objects.all().count() == 0
    assert not SpliceUser.objects.filter(user_id=new_user.user_id).exists()
