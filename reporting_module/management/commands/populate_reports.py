from django.core.management.base import BaseCommand
from reporting_module.models import Report
from admin_module.models import Company

class Command(BaseCommand):
    help = 'Populate initial reports'

    def handle(self, *args, **kwargs):
        company1 = Company.objects.get(name='Apple Inc.')
        company2 = Company.objects.get(name='Google (Alphabet Inc.)')
        company3 = Company.objects.get(name='Microsoft Corporation')
        company4 = Company.objects.get(name='Amazon.com, Inc.')
        company5 = Company.objects.get(name='Tesla, Inc.')

        Report.objects.create(
            company=company1,
            report_date='2024-01-10',
            summary='Quarterly report on Apple Inc.'
        )
        Report.objects.create(
            company=company2,
            report_date='2024-01-11',
            summary='Monthly report on Google'
        )
        Report.objects.create(
            company=company3,
            report_date='2024-01-12',
            summary='Annual report on Microsoft Corporation'
        )
        Report.objects.create(
            company=company4,
            report_date='2024-01-13',
            summary='Overview report on Amazon'
        )
        Report.objects.create(
            company=company5,
            report_date='2024-01-14',
            summary='Sustainability report on Tesla'
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated reports'))
