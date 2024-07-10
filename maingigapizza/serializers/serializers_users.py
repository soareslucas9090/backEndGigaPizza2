from rest_framework import serializers

from ..models import (
    Address,
    Flavors_Pizzas,
    OrderItens,
    OrderPizzas,
    Orders,
    Pizzas,
    Salables,
    Users,
)


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
