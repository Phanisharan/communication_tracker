from django.db import models
from admin_module.models import Company

class Report(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    report_date = models.DateField()
    summary = models.TextField()


