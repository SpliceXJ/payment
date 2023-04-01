from rest_framework import serializers
from splice.users.models.cards import UsersCard
from splice.users.serializers.user_serializer import SpliceUserSerializer


class CardsSerializer(serializers.ModelSerializer):
    owner = SpliceUserSerializer(many=True)

    class Meta:
        model = UsersCard
        fields = [
            "owner",
            "email",
            "first_four_digits",
            "last_four_digits",
            "card_name",
            "card_type",
        ]
