from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from splice.users.models.user import SpliceUser
from splice.users.serializers.user_serializer import SpliceUserSerializer


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def update_user(request):
    user = SpliceUser.objects.get(id=request.user.id)

    if "email" in request.data.keys():
        user.email = request.data["email"]

    if "is_vendor" in request.data.keys():
        user.is_vendor = request.data["is_vendor"]

    user.save()

    return JsonResponse({"data": SpliceUserSerializer(user).data}, status=200)
