from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Categorys, Inputs, Salables, Salables_Compositions, SubCategorys


class CategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = (
            "id",
            "name",
            "is_active",
            "links",
        )

    # Inserção de hiperlinks na resposta
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context["request"]

        links = {}

        # Diferentes links para caso de LIST e RETRIEVE

        if self.context["view"].kwargs:
            links.update({"list": reverse("admin-categories-list", request=request)})

        else:
            links.update(
                {
                    "self": reverse(
                        "admin-categories-detail",
                        kwargs={"pk": obj.pk},
                        request=request,
                    )
                }
            )

        links.update(
            {
                "subcategories": request.build_absolute_uri(
                    reverse("admin-subcategories-list") + f"?category_id={obj.pk}"
                )
            }
        )
        return links


class SubCategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorys
        fields = (
            "id",
            "name",
            "category",
            "is_active",
            "links",
        )

    category = serializers.PrimaryKeyRelatedField(queryset=Categorys.objects.all())

    # Inserção de hiperlinks na resposta
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context["request"]

        links = {}

        # Diferentes links para caso de LIST e RETRIEVE
        if self.context["view"].kwargs:
            links.update({"list": reverse("admin-subcategories-list", request=request)})

        else:
            links.update(
                {
                    "self": reverse(
                        "admin-subcategories-detail",
                        kwargs={"pk": obj.pk},
                        request=request,
                    )
                }
            )

        links.update(
            {
                "category": reverse(
                    "admin-subcategories-detail",
                    kwargs={"pk": obj.category.pk},
                    request=request,
                ),
                "salables": request.build_absolute_uri(
                    reverse("admin-salables-list") + f"?subcategory_id={obj.pk}"
                ),
                "inputs": request.build_absolute_uri(
                    reverse("admin-inputs-list") + f"?subcategory_id={obj.pk}"
                ),
            }
        )
        return links


class InputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inputs
        fields = (
            "id",
            "name",
            "price",
            "quantity",
            "unit",
            "subcategory",
            "is_active",
            "links",
        )

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )

    # Inserção de hiperlinks na resposta
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context["request"]

        links = {}

        # Diferentes links para caso de LIST e RETRIEVE
        if self.context["view"].kwargs:
            links.update({"list": reverse("admin-inputs-list", request=request)})

        else:
            links.update(
                {
                    "self": reverse(
                        "admin-inputs-detail",
                        kwargs={"pk": obj.pk},
                        request=request,
                    )
                }
            )

        links.update(
            {
                "subcategory": reverse(
                    "admin-subcategories-detail",
                    kwargs={"pk": obj.subcategory.pk},
                    request=request,
                ),
                "salables_compositions": request.build_absolute_uri(
                    reverse("admin-salables_compositions-list") + f"?input_id={obj.pk}"
                ),
            }
        )
        return links

    # Retorno de mensagem listando quais as unidades aceitas pelo sistema
    def validate_unit(self, value):
        allowed_units = dict(Inputs.UNITS).keys()
        if value not in allowed_units:
            raise serializers.ValidationError(
                f"'{value}' is not a valid choice. Valid options are:: {', '.join(allowed_units)}"
            )
        return value


class SalablesCompositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salables_Compositions
        fields = (
            "id",
            "input",
            "salable",
            "quantity",
            "links",
        )

    input = serializers.PrimaryKeyRelatedField(queryset=Inputs.objects.all())
    salable = serializers.PrimaryKeyRelatedField(queryset=Salables.objects.all())

    # Inserção de hiperlinks na resposta
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context["request"]

        links = {}

        # Diferentes links para caso de LIST e RETRIEVE
        if self.context["view"].kwargs:
            links.update(
                {"list": reverse("admin-inputs_salables-list", request=request)}
            )

        else:
            links.update(
                {
                    "self": reverse(
                        "admin-inputs_salables-detail",
                        kwargs={"pk": obj.pk},
                        request=request,
                    )
                }
            )

        links.update(
            {
                "input": reverse(
                    "admin-inputs-detail",
                    kwargs={"pk": obj.input.pk},
                    request=request,
                ),
                "salable": reverse(
                    "admin-salables-detail",
                    kwargs={"pk": obj.salable.pk},
                    request=request,
                ),
            }
        )

        return links


class SalablesCompositionsToAdd(serializers.Serializer):
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
            "links",
            "inputs",
        ]

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategorys.objects.all()
    )
    inputs = SalablesCompositionsToAdd(many=True, write_only=True)

    # Inserção de hiperlinks na resposta
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context["request"]

        links = {}

        # Diferentes links para caso de LIST e RETRIEVE
        if self.context["view"].kwargs:
            links.update({"list": reverse("admin-salables-list", request=request)})

        else:
            links.update(
                {
                    "self": reverse(
                        "admin-salables-detail",
                        kwargs={"pk": obj.pk},
                        request=request,
                    )
                }
            )

        links.update(
            {
                "salables_compositions": request.build_absolute_uri(
                    reverse("admin-salables_compositions-list")
                    + f"?salable_id={obj.pk}"
                ),
                "subcategory": reverse(
                    "admin-subcategories-detail",
                    kwargs={"pk": obj.subcategory.pk},
                    request=request,
                ),
            }
        )
        return links

    # Método personalizado para permitir a inserção de
    def create(self, validated_data):
        inputs_data = validated_data.pop("inputs")
        salable = Salables.objects.create(**validated_data)

        for input_data in inputs_data:
            Salables_Compositions.objects.create(
                salable=salable,
                input=input_data["input"],
                quantity=input_data["quantity"],
            )

        return salable

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.subcategory = validated_data.get("subcategory", instance.subcategory)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        # Atualização dos inputs existentes
        if validated_data.get("inputs", None):
            inputs_data = validated_data.pop("inputs")
            # Deletando os inputs antigos
            Salables_Compositions.objects.delete(salable=instance)

            # Adicinando os novos inputs
            for input_data in inputs_data:
                Salables_Compositions.objects.create(
                    salable=instance,
                    input_id=input_data["input"]["id"],
                    quantity=input_data["quantity"],
                )

        return instance
