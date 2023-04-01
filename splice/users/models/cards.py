import uuid
from django.db import models
from splice.users.models.user import SpliceUser


class UsersCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        SpliceUser, related_name="my_cards", on_delete=models.CASCADE
    )
    authorization = models.CharField(max_length=80)
    email = models.EmailField(max_length=200)
    first_four_digits = models.CharField(max_length=4)
    last_four_digits = models.CharField(max_length=4)
    card_name = models.CharField(max_length=200)
    card_type = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.owner.username

    @staticmethod
    def create() -> "UsersCard":
        return
