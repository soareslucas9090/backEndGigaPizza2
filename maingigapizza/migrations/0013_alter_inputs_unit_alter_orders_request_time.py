# Generated by Django 4.2.11 on 2024-07-10 03:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maingigapizza', '0012_alter_inputs_unit_alter_orders_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputs',
            name='unit',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='orders',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 10, 0, 16, 42, 64487)),
        ),
    ]
