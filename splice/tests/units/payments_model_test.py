import pytest
from faker import Faker

from splice.users.models.user import SpliceUser
from splice.payments.models.payments import Payments
from splice.tests.test_helpers.create_test_user import create_test_splice_user
from splice.tests.test_helpers.create_test_payment import create_test_payment


@pytest.mark.django_db
def test_create_payment_instance():
    user_one: SpliceUser = create_test_splice_user()
    user_two: SpliceUser = create_test_splice_user()

    create_test_payment(initiator=user_one, recepient=user_two)
    assert Payments.objects.filter(initiator=user_one).exists()
    assert Payments.objects.filter(recepient=user_two).exists()
    assert Payments.objects.filter(initiator=user_one, recepient=user_two).exists()


@pytest.mark.django_db
def test_payment_instance_remains_after_user_deletion():
    user: SpliceUser = create_test_splice_user()

    payment_instance = create_test_payment(initiator=user)
    assert Payments.objects.filter(initiator=user).exists()
    assert Payments.objects.filter(id=payment_instance.id).exists()

    """ un-comment after user deletion logic is implemented """
    # delete user, check if payment model still exists
    # user.delete()

    # assert Payments.objects.filter(id = payment_instance.id).exists()


@pytest.mark.django_db
def test_payment_instance_updated():
    payment_instance = create_test_payment()
    assert Payments.objects.filter(id=payment_instance.id, is_completed=False).exists()
    assert payment_instance.is_completed is False
    assert payment_instance.reference is None

    payment_instance.is_completed = True
    payment_instance.reference = "TXcV400-12R"
    payment_instance.save()

    assert Payments.objects.filter(id=payment_instance.id, is_completed=True).exists()
    assert payment_instance.is_completed is True
    assert payment_instance.reference is not None


@pytest.mark.django_db
def test_get_spendings_and_earnings():
    user_one: SpliceUser = create_test_splice_user()
    user_two: SpliceUser = create_test_splice_user()

    for amount in [100, 200, 300, 500]:
        # create transaction worth of 1,100 received by user one
        create_test_payment(amount=amount, initiator=user_one, recepient=user_two)

    for amount in [50, 2000]:
        # create transaction worth of 2,050 received by user two
        create_test_payment(amount=amount, initiator=user_two, recepient=user_one)

    user_one_amount_earned = Payments.my_earnings(user_id=user_one.id)
    user_one_amount_spent = Payments.my_spendings(user_id=user_one.id)
    assert round(user_one_amount_earned) == 2050
    assert round(user_one_amount_spent) == 1100

    user_two_amount_earned = Payments.my_earnings(user_id=user_two.id)
    user_two_amount_spent = Payments.my_spendings(user_id=user_two.id)
    assert round(user_two_amount_earned) == 1100
    assert round(user_two_amount_spent) == 2050
