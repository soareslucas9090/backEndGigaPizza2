from rest_framework import serializers

from ..models import Inputs_Salables, Salables, Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ["last_login", "address", "is_admin", "is_active"]

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password


class SalablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salables
        fields = [
            "name",
            "description",
            "price",
            "subcategory",
            "category",
        ]

    subcategory = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_subcategory(self, obj):
        try:
            return obj.subcategory.name
        except:
            return None

    def get_category(self, obj):
        try:
            return obj.subcategory.category.name
        except:
            return None
