from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from splice.users.models.cards import UsersCard
from splice.users.serializers.cards_serializer import CardsSerializer


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_my_cards(request):
    cards = UsersCard.objects.filter(owner__id=request.user.id)

    if cards.exists():
        return JsonResponse(
            {"data": CardsSerializer(cards, many=True).data}, status=200
        )

    return JsonResponse({}, status=201)
