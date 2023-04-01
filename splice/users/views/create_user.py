from django.http import JsonResponse
from rest_framework.decorators import api_view
from splice.users.models.user import SpliceUser
from splice.users.serializers.user_serializer import SpliceUserSerializer


@api_view(["POST"])
def create_user(request):
    serializer = SpliceUserSerializer(request.data)
    if serializer.is_valid():
        new_user = SpliceUser.creare(
            firstname=request.data.firstname,
            lastname=request.data.lastname,
            email=request.data.email,
            username=request.data.username,
        )
        return JsonResponse(
            {"transaction_id": new_user.get_transaction_id()}, status=200
        )
    return JsonResponse(serializer.errors, status=400)
