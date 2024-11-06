# Generated by Django 4.1.13 on 2024-11-05 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0004_alter_customer_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 11, 5, 13, 14, 40, 604525, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date Created",
            ),
        ),
    ]
