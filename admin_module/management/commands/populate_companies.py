from admin_module.models import Company, CommunicationMethod, Communication
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate companies and communications'

    def handle(self, *args, **kwargs):
        communications_data = [
            {'company_name': 'Apple Inc.', 'method_name': 'Email', 'date': '2025-01-01', 'notes': 'Sent an email about upcoming event', 'due_date': '2025-06-01'},  # Scheduled
            {'company_name': 'Google (Alphabet Inc.)', 'method_name': 'Phone Call', 'date': '2025-01-03', 'notes': 'Called to discuss collaboration', 'due_date': '2025-01-03'},  # Completed
            {'company_name': 'Microsoft Corporation', 'method_name': 'LinkedIn Post', 'date': '2025-01-07', 'notes': 'LinkedIn post about new service', 'due_date': '2025-05-01'},  # Scheduled
            {'company_name': 'Amazon.com, Inc.', 'method_name': 'Email', 'date': '2025-01-08', 'notes': 'Email about partnership opportunities', 'due_date': '2025-01-08'},  # Completed
            {'company_name': 'Tesla, Inc.', 'method_name': 'LinkedIn Post', 'date': '2025-01-14', 'notes': 'LinkedIn post about new Tesla model', 'due_date': '2025-07-01'},  # Scheduled
        ]

        for comm in communications_data:
            try:
                company = Company.objects.get(name=comm['company_name'])
                method = CommunicationMethod.objects.get(name=comm['method_name'])
                comm_date = datetime.strptime(comm['date'], '%Y-%m-%d').date()
                due_date = make_aware(datetime.strptime(comm['due_date'], '%Y-%m-%d'))

                # Create communication record
                Communication.objects.create(
                    company=company,
                    method=method,
                    date=comm_date,
                    notes=comm['notes'],
                    due_date=due_date,
                )
                print(f"Successfully added communication for {comm['company_name']} with status.")
            except Company.DoesNotExist:
                print(f"Company {comm['company_name']} does not exist.")
            except CommunicationMethod.DoesNotExist:
                print(f"Method {comm['method_name']} does not exist.")
            except Exception as e:
                print(f"Error while adding communication: {e}")
