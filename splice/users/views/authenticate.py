from django.http import JsonResponse
from rest_framework.decorators import api_view

from splice.users.models.user import SpliceUser
from rest_framework.authtoken.models import Token


@api_view(["POST"])
def get_auth_token(request):
    # add serializer validation here
    try:
        auth_user = SpliceUser.objects.get(username=request.data["user_id"])

        """ compare transaction ID received and user's transaction ID """

        if request.data["transaction_id"] != auth_user.get_transaction_id():
            return JsonResponse({"message": "Invalid Auth Credentials"}, status=400)
    except:
        return JsonResponse({"message": "Invalid Auth Credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=auth_user)
    return JsonResponse({"Authorization": token.key}, status=200)
