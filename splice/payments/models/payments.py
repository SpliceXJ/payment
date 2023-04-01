import uuid
from typing import Union
from django.db import models
from splice.users.models.user import SpliceUser


class Payments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(blank=False)
    reference = models.CharField(max_length=100)
    initiator = models.ForeignKey(
        SpliceUser, related_name="spent_cash", on_delete=models.PROTECT
    )
    receipient = models.ForeignKey(
        SpliceUser, related_name="received_cash", on_delete=models.PROTECT
    )
    is_completed = models.BooleanField(default=True, blank=False)

    def __str__(self) -> str:
        return f"{self.initiator.email} to {self.receipient.email}"

    @staticmethod
    def create(
        amount: Union[int, float],
        initiator: "SpliceUser",
        receipient: "SpliceUser",
        reference: str,
    ) -> "Payments":
        return Payments.objects.create(
            amount=amount,
            reference=reference,
            initiator=initiator,
            receipient=receipient,
        )

    @staticmethod
    def my_earnings(user_id: uuid.UUID) -> int:
        total = 0.00
        earnings = Payments.objects.filter(recepient__id=user_id).all()
        if not earnings.exists():
            return total
        for earning in earnings:
            total += earning.amount
        return total

    @staticmethod
    def my_spendings(user_id: uuid.UUID) -> int:
        total = 0.00
        spendings = Payments.objects.filter(initiator__id=user_id).all()
        if not spendings.exists():
            return total
        for spending in spendings:
            total += spending.amount
        return total
