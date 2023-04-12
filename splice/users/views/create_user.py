from django.http import JsonResponse
from rest_framework.decorators import api_view
from splice.users.models.user import SpliceUser
from splice.users.serializers.user_serializer import SpliceUserSerializer


@api_view(["POST"])
def create_user(request):
    serializer = SpliceUserSerializer(data=request.data)
    # if serializer.is_valid():
    if "email" in request.data.keys() and "user_id" in request.data.keys():
        new_user = SpliceUser.create(
            email=request.data["email"],
            username=request.data["user_id"],
        )
        return JsonResponse(
            {
                "transaction_id": new_user.get_transaction_id(),
                "data": SpliceUserSerializer(new_user).data,
            },
            status=200,
        )
    return JsonResponse({"message": "email amd user_id required"}, status=400)
    # return JsonResponse(serializer.errors, status=400)
