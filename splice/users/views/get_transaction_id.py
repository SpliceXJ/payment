from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from splice.users.models.user import SpliceUser


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_transaction_id(request):
    # fetch request user from token here
    try:
        transaction_id = SpliceUser.objects.get(
            username=request.user.username
        ).get_transaction_id()

        return JsonResponse({"transaction_id": transaction_id}, status=200)
    except SpliceUser.DoesNotExist:
        return JsonResponse({"message": "account does not exist"}, status=400)
