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
        fields = ["input", "input_name", "quantity"]

    input_name = serializers.CharField(source="input.name", read_only=True)
    input = serializers.PrimaryKeyRelatedField(queryset=Inputs.objects.all())


class SalablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salables
        fields = [
            "id",
            "name",
            "description",
            "price",
            "subcategory",
            "is_active",
            "inputs",
        ]

    inputs = InputsSalablesSerializer(many=True)
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )

    def create(self, validated_data):
        inputs_data = validated_data.pop("inputs")
        salable = Salables.objects.create(**validated_data)

        for input_data in inputs_data:
            Inputs_Salables.objects.create(
                salable=salable,
                input=input_data["input"],
                quantity=input_data["quantity"],
            )

        return salable

    def update(self, instance, validated_data):
        inputs_data = validated_data.pop("inputs")

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.subcategory = validated_data.get("subcategory", instance.subcategory)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        # Delete existing inputs
        instance.inputs.clear()

        # Add new inputs
        for input_data in inputs_data:
            Inputs_Salables.objects.create(
                salable=instance,
                input_id=input_data["input"]["id"],
                quantity=input_data["quantity"],
            )

        return instance


class Flavors_PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavors_Pizzas
        fields = "__all__"


class PizzasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizzas
        fields = "__all__"

    flavors = serializers.PrimaryKeyRelatedField(
        queryset=Salables.objects.all(), many=True, required=True
    )
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        flavors = validated_data.pop("flavors", [])
        names = ""

        if len(flavors) == 1:
            names = flavors[0]

        if len(flavors) == 2:
            names = f"{flavors[0]} + {flavors[1]}"

        if len(flavors) == 3:
            names = f"{flavors[0]} + {flavors[1]} + {flavors[2]}"

        validated_data["name"] = names

        pizza = Pizzas.objects.create(**validated_data)

        return pizza


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
