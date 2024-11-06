# Generated by Django 4.1.13 on 2024-11-05 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="Last Name"),
                ),
                (
                    "mssisdn",
                    models.CharField(max_length=50, verbose_name="MSSISDN Number"),
                ),
                (
                    "profession",
                    models.CharField(max_length=100, verbose_name="Profession"),
                ),
                (
                    "id_number",
                    models.CharField(max_length=100, verbose_name="ID Number"),
                ),
                (
                    "id_picture",
                    models.CharField(max_length=200, verbose_name="Photo of ID"),
                ),
                ("address", models.CharField(max_length=200, verbose_name="Address")),
                (
                    "nationality",
                    models.CharField(max_length=100, verbose_name="Nationality"),
                ),
                (
                    "id_type",
                    models.ForeignKey(
                        blank=True,
                        default=["Passport"],
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.idtype",
                    ),
                ),
                (
                    "sim_type",
                    models.ForeignKey(
                        blank=True,
                        default=["Passport"],
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.simtype",
                    ),
                ),
            ],
        ),
    ]
