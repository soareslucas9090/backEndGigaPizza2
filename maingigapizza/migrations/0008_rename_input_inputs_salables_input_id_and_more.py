# Generated by Django 4.2.11 on 2024-07-08 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maingigapizza', '0007_alter_orders_request_time_alter_salables_inputs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inputs_salables',
            old_name='input',
            new_name='input_id',
        ),
        migrations.RenameField(
            model_name='inputs_salables',
            old_name='salable',
            new_name='salable_id',
        ),
        migrations.AlterField(
            model_name='orders',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 8, 14, 59, 45, 624061)),
        ),
    ]
