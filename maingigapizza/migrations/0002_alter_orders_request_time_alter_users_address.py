# Generated by Django 4.2.11 on 2024-07-06 17:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maingigapizza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='request_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 6, 14, 44, 39, 474811)),
        ),
        migrations.AlterField(
            model_name='users',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='maingigapizza.address'),
        ),
    ]
