from rest_framework import serializers

from ..models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ["last_login", "addreess", "is_admin", "is_active"]

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password
