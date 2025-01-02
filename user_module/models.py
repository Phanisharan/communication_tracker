from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')])
    is_active = models.BooleanField(default=True)

