import uuid
from typing import Union
from django.db import models
from splice.users.models.user import SpliceUser


class UsersCard(models.Model):
    """user can only have 3 cards stored, be sure to add that check"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        SpliceUser, related_name="my_cards", on_delete=models.CASCADE
    )
    authorization = models.CharField(max_length=80)
    email = models.EmailField(max_length=200)
    first_four_digits = models.CharField(max_length=4)
    last_four_digits = models.CharField(max_length=4)
    card_type = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.owner.username

    @staticmethod
    def create(
        owner: SpliceUser,
        authorization: str,
        email: str,
        first_four_digits: Union[str, int],
        last_four_digits: Union[str, int],
        card_type: str,
    ) -> "UsersCard":
        return UsersCard.objects.create(
            owner=owner,
            authorization=authorization,
            email=email,
            first_four_digits=first_four_digits,
            last_four_digits=last_four_digits,
            card_type=card_type,
        )
