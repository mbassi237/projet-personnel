from django.contrib import admin
from .models import Patient, Frottis, Rapport 

# Register your models here.
admin.site.register(Patient)
admin.site.register(Frottis)
admin.site.register(Rapport)