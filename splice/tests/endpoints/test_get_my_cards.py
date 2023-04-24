import pytest
from rest_framework.test import APIClient

from splice.users.models.user import SpliceUser
from splice.users.models.cards import UsersCard
from splice.tests.test_helpers.create_test_card import create_test_card
from splice.tests.test_helpers.create_test_user import create_test_splice_user


@pytest.mark.django_db
class TestGetMyCards:
    def setup_method(self, method):
        self.user: SpliceUser = create_test_splice_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = "/users/get-my-cards/"

    def test_get_my_cards(self):
        # create credit cards for logged in user
        for _ in range(3):
            create_test_card(owner=self.user)

        assert UsersCard.objects.filter(owner=self.user).count() == 3

        response = self.client.get(path=self.url)

        assert response.status_code == 200
        assert len(response.json()["data"]) == 3
