from django.http import JsonResponse
from splice.payments.models.payments import Payments
from splice.payments.serializers.payments_serializer import PaymentsModelSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_payment_history(request):
    my_payments = Payments.objects.filter(initiator__id=request.user.id)

    if my_payments.exists():
        return JsonResponse(
            {"data": PaymentsModelSerializer(my_payments, many=True).data}, status=200
        )
    
    return JsonResponse({}, status=201)