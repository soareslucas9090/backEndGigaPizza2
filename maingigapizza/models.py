from datetime import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models


class Categorys(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}"


class SubCategorys(models.Model):
    name = models.CharField(max_length=255, null=False, unique=False)
    category = models.ForeignKey(
        Categorys,
        related_name="principal_category",
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}"


class Inputs(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField(null=False)
    quantity = models.FloatField(null=False)
    unit = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}"


class Salables(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(null=False)
    subcategory = models.ForeignKey(
        SubCategorys, on_delete=models.CASCADE, related_name="subcategory", null=False
    )
    is_active = models.BooleanField(default=True, null=False)
    inputs = models.ManyToManyField(
        "Inputs", through="Inputs_Salables", related_name="salables"
    )

    def __str__(self):
        return f"{self.name}"


class Inputs_Salables(models.Model):
    salable = models.ForeignKey(
        Salables,
        on_delete=models.RESTRICT,
        related_name="salable",
    )
    input = models.ForeignKey(
        Inputs,
        on_delete=models.RESTRICT,
        related_name="inputs",
    )
    quantity = models.FloatField(null=False)

    def __str__(self):
        return f"Inputs_Salables {self.salable}, {self.input}, {self.quantity}"


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
            **extra_fields,
        )

        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        user.is_admin = True
        user.is_superuser = True

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=11, null=False, unique=True)
    tel = models.CharField(max_length=11, null=False)
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
    request_time = models.DateTimeField(null=False, default=datetime.now())
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
