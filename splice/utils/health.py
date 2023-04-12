from django.urls import path
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"message": "active"}, status=200)


urlpatterns = [
    path("check/", health_check),
]
