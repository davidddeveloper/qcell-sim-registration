from django.contrib import admin
from .models import IDType, Customer, SimType, Gender

# Register your models here.
admin.site.register(Customer)
admin.site.register(IDType)
admin.site.register(SimType)
admin.site.register(Gender)