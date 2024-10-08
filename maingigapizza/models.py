from datetime import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models


def selfCapitalize(str):
    p = [
        "da",
        "de",
        "do",
        "para",
    ]

    items = []
    for item in str.split():
        if not item in p:
            item = item.capitalize()
        items.append(item)

    new_name = " ".join(items)
    return new_name


class CategoryTypes(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = selfCapitalize(self.name)
        super().save(*args, **kwargs)


class Categories(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    type = models.ForeignKey(
        CategoryTypes,
        related_name="type_category",
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "type"], name="unique_name_type_constraint"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = selfCapitalize(self.name)
        super().save(*args, **kwargs)


class SubCategories(models.Model):
    name = models.CharField(max_length=255, null=False, unique=False)
    category = models.ForeignKey(
        Categories,
        related_name="principal_category",
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_name_category_constraint"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = selfCapitalize(self.name)
        super().save(*args, **kwargs)


class Inputs(models.Model):
    UNITS = [
        ("kg", "Kilo"),
        ("g", "Gram"),
        ("mg", "Miligram"),
        ("l", "Liter"),
        ("ml", "Mililiter"),
        ("und", "Unit"),
    ]

    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField(null=False)
    quantity = models.FloatField(null=False)
    unit = models.CharField(max_length=3, null=False)
    subcategory = models.ForeignKey(
        SubCategories,
        on_delete=models.CASCADE,
        related_name="inputs_subcategory",
        null=False,
    )
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "subcategory"],
                name="unique_name_subcategory_in_inputs_constraint",
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = selfCapitalize(self.name)
        super().save(*args, **kwargs)


class Salables(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(null=False)
    subcategory = models.ForeignKey(
        SubCategories, on_delete=models.CASCADE, related_name="subcategory", null=False
    )
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "subcategory"],
                name="unique_name_subcategory_in_salables_constraint",
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Salables_Compositions(models.Model):
    salable = models.ForeignKey(Salables, on_delete=models.RESTRICT)
    input = models.ForeignKey(Inputs, on_delete=models.RESTRICT)
    quantity = models.FloatField(null=False)

    def __str__(self):
        return f"Salables_Compositions {self.salable}, {self.input}, {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["salable", "input"],
                name="unique_salable_composition_input_constraint",
            )
        ]


class Pizzas(models.Model):
    name = models.CharField(max_length=255, null=False)
    size = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    flavors = models.ManyToManyField(Salables, through="Flavors_Pizzas")

    def __str__(self):
        return f"Pizza {self.name}"


class Flavors_Pizzas(models.Model):
    pizza = models.ForeignKey(
        Pizzas, on_delete=models.RESTRICT, related_name="pizza", null=False
    )

    salable = models.ForeignKey(
        Salables, on_delete=models.RESTRICT, related_name="salablePizza", null=False
    )

    def __str__(self):
        return f"Pizza {self.name}"


class Address(models.Model):
    street = models.CharField(max_length=255, null=False)
    neighborhood = models.CharField(max_length=255, null=False)
    number = models.IntegerField(null=False)
    complent = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True, null=False)


class UserManager(BaseUserManager):
    def create_user(
        self,
        name,
        email,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        name,
        email,
        password=None,
        **extra_fields,
    ):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            password=password,
            is_admin=True,
            is_superuser=True,
            **extra_fields,
        )

        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=11, null=False, unique=True)
    tel = models.CharField(max_length=11, null=False, unique=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="address", null=True
    )
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=512, null=False)
    is_admin = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)

    REQUIRED_FIELDS = [
        "name",
        "cpf",
    ]

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        str = f"{self.email}"
        return str

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        super().save(*args, **kwargs)


class Orders(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.RESTRICT, related_name="user", null=False
    )
    request_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField()
    description = models.CharField(max_length=512, null=False)
    is_finished = models.BooleanField(default=False)


class OrderItens(models.Model):
    salable = models.ForeignKey(
        Salables,
        on_delete=models.RESTRICT,
    )
    order = models.ForeignKey(
        Orders,
        on_delete=models.RESTRICT,
    )
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


class OrderPizzas(models.Model):
    pizza = models.ForeignKey(
        Pizzas,
        on_delete=models.RESTRICT,
    )
    order = models.ForeignKey(
        Orders,
        on_delete=models.RESTRICT,
    )
