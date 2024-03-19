from rest_framework import serializers

from .models import *


class CategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = "__all__"


class SubCategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorys
        fields = "__all__"

    category = serializers.PrimaryKeyRelatedField(queryset=Categorys.objects.all())


class InputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inputs
        fields = "__all__"


class InputsSalablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inputs_Salables
        fields = "__all__"

    salable = serializers.PrimaryKeyRelatedField(queryset=Salables.objects.all())
    input = serializers.PrimaryKeyRelatedField(queryset=Inputs.objects.all())


class SalablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salables
        fields = "__all__"

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )


class PizzasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizzas
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ["last_login"]

        extra_kwargs = {
            "is_admin": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password


class Users2AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ["last_login"]

        extra_kwargs = {
            "is_superuser": {"read_only": True},
        }

    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    def validate_password(self, value):
        password = value

        if len(password) < 8:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())


class OrderItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItens
        fields = "__all__"

    salable = serializers.PrimaryKeyRelatedField(queryset=Salables.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())


class OrderPizzasSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItens
        fields = "__all__"

    pizza = serializers.PrimaryKeyRelatedField(queryset=Pizzas.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
