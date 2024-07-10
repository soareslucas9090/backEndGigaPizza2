from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema_field
from rest_framework import serializers

from ..models import Categorys, Inputs, Inputs_Salables, Salables, SubCategorys


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

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )

    def validate_unit(self, value):
        allowed_units = dict(Inputs.UNITS).keys()
        if value not in allowed_units:
            raise serializers.ValidationError(
                f"'{value}' is not a valid choice. Valid options are:: {', '.join(allowed_units)}"
            )
        return value


class InputsSalablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inputs_Salables
        fields = "__all__"

    input = serializers.PrimaryKeyRelatedField(queryset=Inputs.objects.all())
    salable = serializers.PrimaryKeyRelatedField(queryset=Salables.objects.all())


class InputsSalablesToAdd(serializers.Serializer):
    input = serializers.PrimaryKeyRelatedField(queryset=Inputs.objects.all())
    quantity = serializers.FloatField(required=True)


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

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )
    inputs = InputsSalablesToAdd(many=True, write_only=True)

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
