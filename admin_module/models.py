from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    linkedin_profile = models.URLField()
    emails = models.JSONField(default=list)
    phone_numbers = models.JSONField(default=list)
    comments = models.TextField(blank=True)
    communication_periodicity = models.IntegerField(default=14)

class CommunicationMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sequence = models.IntegerField()
    is_mandatory = models.BooleanField(default=False)

class Communication(models.Model):

    STATUS_CHOICES = [
        ('overdue', 'Overdue'),
        ('completed', 'Completed'),
        ('scheduled', 'Scheduled'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    method = models.ForeignKey(CommunicationMethod, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    due_date = models.DateTimeField(null=True)


    def save(self, *args, **kwargs):
        if self.due_date:
            now = timezone.now()
            if self.due_date < now:
                self.status = 'overdue'
            elif self.due_date > now:
                self.status = 'scheduled'
            else:
                self.status = 'completed'
        super().save(*args, **kwargs)