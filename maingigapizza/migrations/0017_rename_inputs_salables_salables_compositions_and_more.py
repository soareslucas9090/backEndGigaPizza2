# Generated by Django 4.2.14 on 2024-07-15 14:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maingigapizza', '0016_inputs_subcategory_alter_orders_request_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Inputs_Salables',
            new_name='Salables_Compositions',
        ),
        migrations.AlterField(
            model_name='inputs',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs_subcategory', to='maingigapizza.subcategorys'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 15, 11, 50, 47, 945780)),
        ),
    ]
