from django.apps import AppConfig
from django.db import OperationalError
from django.db.models.signals import post_migrate


class MaingigapizzaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maingigapizza"

    def ready(self):
        from .models import CategoryTypes

        post_migrate.connect(create_default_category_types, sender=self)


def create_default_category_types(sender, **kwargs):
    CategoryType = sender.get_model("CategoryTypes")
    default_types = ["Insumos", "P/ Venda", "Taxas"]

    for type_name in default_types:
        try:
            CategoryType.objects.get_or_create(name=type_name)
        except OperationalError:
            pass
