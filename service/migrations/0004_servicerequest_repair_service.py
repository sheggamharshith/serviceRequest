# Generated by Django 4.2 on 2023-04-16 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0003_servicerequest_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicerequest",
            name="repair_service",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="service.repairservice",
            ),
            preserve_default=False,
        ),
    ]