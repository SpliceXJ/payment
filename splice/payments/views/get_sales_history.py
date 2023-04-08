from django.http import JsonResponse
from splice.payments.models.payments import Payments
from splice.payments.serializers.payments_serializer import PaymentsModelSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_sales_history(request):
    my_sales = Payments.objects.filter(recepient__id=request.user.id)

    if my_sales.exists():
        return JsonResponse(
            {"data": PaymentsModelSerializer(my_sales, many=True).data}, status=200
        )

    return JsonResponse({}, status=201)
