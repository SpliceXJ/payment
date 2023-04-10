import os
from dotenv import load_dotenv

load_dotenv()

import uuid
import requests
from django.http import JsonResponse
from splice.utils.save_card import save_payment_card

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

URL = os.getenv("VERIFY_PAYMENT_URL")


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def verify_payment(request):
    from splice.payments.models.payments import Payments

    reference: str = request.data["reference"]
    save_card: bool = request.data["save_card"]

    response = requests.get(
        url=URL + reference,
        headers={
            "authorization": f'Bearer {os.getenv("PAYMENT_SECRET_KEY")}',
            "content-type": "application/json",
            "cache-control": "no-cache",
        },
    )

    data = response.json()
    if data.data.status != "success":
        return JsonResponse({"message": "transaction not successful"}, status=400)

    if save_card:
        save_payment_card(data=data)

    payment_id = uuid.UUID(request.data["payment_instance_id"])
    payment_instance = Payments.objects.get(id=payment_id)

    payment_instance.is_completed = True
    payment_instance.reference = request.data["reference"]
    payment_instance.save()

    return JsonResponse({"message": "transaction successful"}, status=200)
