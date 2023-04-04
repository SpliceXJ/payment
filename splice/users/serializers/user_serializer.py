from rest_framework import serializers
from splice.users.models.user import SpliceUser


class SpliceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpliceUser
        fields = [
            "username",
            "user_id",
            "email",
            "is_vendor",
            "created_at",
            "updated_at",
        ]
