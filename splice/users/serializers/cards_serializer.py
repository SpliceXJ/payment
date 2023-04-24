from rest_framework import serializers
from splice.users.models.cards import UsersCard
from splice.users.serializers.user_serializer import SpliceUserSerializer


class CardsSerializer(serializers.ModelSerializer):
    owner = SpliceUserSerializer(many=False)

    class Meta:
        model = UsersCard
        fields = [
            "owner",
            "email",
            "last_four_digits",
            "card_type",
        ]
