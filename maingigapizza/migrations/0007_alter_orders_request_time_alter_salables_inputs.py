# Generated by Django 4.2.11 on 2024-07-08 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maingigapizza', '0006_alter_inputs_salables_input_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 8, 14, 59, 15, 791309)),
        ),
        migrations.AlterField(
            model_name='salables',
            name='inputs',
            field=models.ManyToManyField(through='maingigapizza.Inputs_Salables', to='maingigapizza.inputs'),
        ),
    ]
