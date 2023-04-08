from rest_framework.serializers import ModelSerializer

from splice.users.serializers.user_serializer import SpliceUserSerializer

from splice.payments.models.payments import Payments

class PaymentsModelSerializer(ModelSerializer):
    initiator = SpliceUserSerializer(many=False)
    recepient = SpliceUserSerializer(many=False)

    class Meta:
        model = Payments
        fields = [
            "amount",
            "item_name",
            "initiator",
            "recepient",
            "created_at",
            "is_completed"
        ]