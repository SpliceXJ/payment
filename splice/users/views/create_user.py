from django.http import JsonResponse
from rest_framework.decorators import api_view
from splice.users.models.user import SpliceUser
from splice.users.serializers.user_serializer import SpliceUserSerializer


@api_view(["POST"])
def create_user(request):
    serializer = SpliceUserSerializer(data=request.data)
    if serializer.is_valid():
        new_user = SpliceUser.create(
            email=serializer.data["email"],
            username=serializer.data["username"],
        )
        return JsonResponse(
            {
            "transaction_id": new_user.get_transaction_id(),
            "data": SpliceUserSerializer(new_user).data
            },
            status=200
        )
    return JsonResponse(serializer.errors, status=400)
