from django.contrib import admin
from .models import Company, Communication, CommunicationMethod

# Register your models here.
admin.site.register(Company)
admin.site.register(Communication)
admin.site.register(CommunicationMethod)

