import django
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


GENDERS = {
    "m": "Male",
    "f": "Female"
}

SIM_TYPES = {
    "esim": "Embedded Sim",
    "standard": "Standard Sim"
}

ID_TYPES = {
    "nin": "National ID",
    "pp": "Passport",
    "vi": "Voters ID",
    "lic": "License"
}

class Customer(models.Model):
    """
        Represent a new Qcell customer
        Attributes:
            - first_name: customer first name
            - last_name: customer last name
            - other name: middle name
            - mssisdn: mssisdn in sim
            - profession: customer profession
            - id_number: number in identity card
            - id_type: type id of identity card
            - address: customer address
            - nationality: customer nationality
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #sim_type = models.ForeignKey(to=SimType, verbose_name="Sim Type", blank=True, on_delete=models.CASCADE, default=["Passport"])
    sim_type = models.CharField(max_length=15, choices=SIM_TYPES)
    first_name = models.CharField("First Name", max_length=50)
    middle_name = models.CharField("Middle Name", max_length=50, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=50)
    gender = models.CharField(max_length=7, choices=GENDERS, default='m')
    mssisdn = models.CharField("Phone Number", max_length=15)  # Mobile Station International Subscriber Directory Numbe
    profession = models.CharField("Profession", max_length=100)
    id_number = models.CharField("ID Number", max_length=100)
    #id_type = models.ForeignKey(to=IDType, verbose_name="ID Type", blank=True, on_delete=models.CASCADE, default=["Passport"])
    id_type = models.CharField(max_length=15, choices=ID_TYPES)
    id_picture = models.CharField("Photo of ID", max_length=200)
    address = models.CharField("Address", max_length=200)
    nationality = models.CharField("Nationality", max_length=100)
    date_created = models.DateTimeField(verbose_name="Date Created", default=django.utils.timezone.now)
    agent = models.ForeignKey(to=User, verbose_name="Agent", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

