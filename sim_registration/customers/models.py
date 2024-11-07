import django
import datetime
import uuid
from django.db import models

# Create your models here.
class IDType(models.Model):
    """
        Represent ID TYPE

        Attributes:
            - name: name of id type (eg. passport)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SimType(models.Model):
    """
        Represent ID TYPE

        Attributes:
            - name: name of id type (eg. passport)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    sim_type = models.ForeignKey(to=SimType, verbose_name="Sim Type", blank=True, on_delete=models.CASCADE, default=["Passport"])
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    mssisdn = models.CharField("MSSISDN Number", max_length=50)
    profession = models.CharField("Profession", max_length=100)
    id_number = models.CharField("ID Number", max_length=100)
    id_type = models.ForeignKey(to=IDType, verbose_name="ID Type", blank=True, on_delete=models.CASCADE, default=["Passport"])
    id_picture = models.CharField("Photo of ID", max_length=200)
    address = models.CharField("Address", max_length=200)
    nationality = models.CharField("Nationality", max_length=100)
    date_created = models.DateTimeField(verbose_name="Date Created", default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
