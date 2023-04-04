import uuid
from django.http import JsonResponse
from rest_framework.decorators import api_view

from splice.users.models.user import SpliceUser
from rest_framework.authtoken.models import Token


@api_view(["POST"])
def get_auth_token(request):
    # add serializer validation here
    try:   
        auth_user = SpliceUser.objects.get(
            username=request.data["username"]
        )

        if request.data["transaction_id"] != auth_user.get_transaction_id():
            return JsonResponse({"message": "Invalid Auth Credentials"}, status=400)
    except:
        return JsonResponse({"message": "Invalid Auth Credentials"}, status=400)
    
    token = Token.objects.create(user=auth_user)
    
    return JsonResponse({"Authorization": token.key}, status=200)
