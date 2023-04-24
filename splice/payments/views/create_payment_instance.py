from django.http import JsonResponse
from splice.payments.models.payments import Payments
from splice.users.models.user import SpliceUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from splice.payments.serializers.payments_serializer import PaymentsModelSerializer


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_payment_instance(request):
    # get initiator
    initiator = SpliceUser.objects.get(id=request.user.id)

    # get recepient
    try:
        # id of the user created on the nodejs app is stored in username field in django
        recepient = SpliceUser.objects.get(username=request.data["recepient_id"])
        if recepient.get_transaction_id() != request.data["recepient_transaction_id"]:
            return JsonResponse(
                {"message": "recepient transaction id invalid"}, status=400
            )
    except SpliceUser.DoesNotExist:
        return JsonResponse({"message": "recepient does not exist"}, status=401)

    # create instance
    new_instance = Payments.create(
        amount=request.data["amount"],
        initiator=initiator,
        recepient=recepient,
        item_id=request.data["item_id"],
    )

    return JsonResponse(
        PaymentsModelSerializer(new_instance, many=False).data, status=200
    )
