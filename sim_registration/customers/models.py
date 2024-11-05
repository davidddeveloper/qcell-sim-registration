from django.db import models

# Create your models here.
class IDType(models.Model):
    """
        Represent ID TYPE

        Attributes:
            - name: name of id type (eg. passport)
    """
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
    first_name = models.CharField("FirstName", max_length=50)
    last_name = models.CharField("LastName", max_length=50)
    mssisdn = models.CharField("Phone Number (mssidn number)", max_length=50)
    profession = models.CharField("Profession", max_length=100)
    id_number = models.CharField("ID Number", max_length=100)
    id_type = models.ManyToManyField(to=IDType, blank=True)
    id_picture = models.CharField("Photo of ID", max_length=200)
    address = models.CharField("Address", max_length=200)
    nationality = models.CharField("Nationality", max_length=100)
