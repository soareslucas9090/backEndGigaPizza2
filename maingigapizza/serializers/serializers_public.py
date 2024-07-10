from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ..models import Inputs_Salables, Salables, Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = [
            "last_login",
            "address",
            "is_admin",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
        ]

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        password256 = make_password(password=password)

        return password256


class SalablesPublicSerializer(serializers.ModelSerializer):
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

    @extend_schema_field(serializers.CharField)
    def get_subcategory(self, obj):
        try:
            return obj.subcategory.name
        except:
            return None

    @extend_schema_field(serializers.CharField)
    def get_category(self, obj):
        try:
            return obj.subcategory.category.name
        except:
            return None
