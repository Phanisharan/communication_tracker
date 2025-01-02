from django.core.management.base import BaseCommand
from user_module.models import User

class Command(BaseCommand):
    help = 'Populate initial users'

    def handle(self, *args, **kwargs):
        User.objects.create(username='john_doe', email='john.doe@example.com', password='password123', role='User')
        User.objects.create(username='jane_doe', email='jane.doe@example.com', password='password123', role='Admin')
        self.stdout.write(self.style.SUCCESS('Successfully populated users'))
