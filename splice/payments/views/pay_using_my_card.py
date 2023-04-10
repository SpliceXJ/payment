import os
from dotenv import load_dotenv

load_dotenv()

import uuid
import requests
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

URL = os.getenv("RECURRENT_PAYMENT_URL")


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def pay_with_saved_card(request):
    from splice.payments.models.payments import Payments
    from splice.users.models.cards import UsersCard

    payment_id = uuid.UUID(request.data["payment_instance_id"])
    payment_instance = Payments.objects.get(id=payment_id)

    card_id = uuid.UUID(request.data["card_id"])
    card = UsersCard.objects.get(id=card_id)

    form = {
        "authorization_code": card.authorization,
        "email": card.email,
        "amount": payment_instance.amount,
    }

    response = requests.post(
        url=URL,
        headers={
            "authorization": f'Bearer {os.getenv("PAYMENT_SECRET_KEY")}',
            "content-type": "application/json",
            "cache-control": "no-cache",
        },
        data=form,
    )

    data = response.json()

    if data.data.status != "success":
        return JsonResponse({"message": "transaction not successful"}, status=400)

    payment_instance.is_completed = True
    payment_instance.reference = data.data.reference  # reference from charge
    payment_instance.save()

    return JsonResponse({"message": "transaction successful"}, status=200)
