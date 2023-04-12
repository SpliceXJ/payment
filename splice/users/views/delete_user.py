from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from splice.users.models.user import SpliceUser


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def delete_user(request):
    try:
        SpliceUser.objects.get(id=request.user.id).delete()
        return JsonResponse({"message": "deleted successfully"}, status=200)
    except SpliceUser.DoesNotExist:
        return JsonResponse({"message": "deletion un-successful"}, status=400)
