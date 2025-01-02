from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Report
from .serializers import ReportSerializer
import csv

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# View for downloading CSV report
def download_csv_report(request):
    reports = Report.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'

    writer = csv.writer(response)
    writer.writerow(['Company', 'Report Date', 'Summary'])

    for report in reports:
        writer.writerow([report.company.name, report.report_date, report.summary])

    return response

# View for downloading PDF report
def download_pdf_report(request):
    # Implementation for downloading PDF report (use a library like ReportLab)
    pass

# Communication Frequency View
class CommunicationFrequencyView(APIView):
    def get(self, request):
        # Your logic to gather communication frequency data
        data = {
            'labels': ['LinkedIn Post', 'Email', 'Phone Call'],
            'datasets': [{
                'label': 'Frequency',
                'data': [10, 20, 5]
            }]
        }
        return Response(data)

# Engagement Effectiveness View
class EngagementEffectivenessView(APIView):
    def get(self, request):
        # Your logic to gather engagement effectiveness data
        data = {
            'labels': ['LinkedIn Post', 'Email', 'Phone Call'],
            'datasets': [{
                'label': 'Effectiveness',
                'data': [70, 50, 30]
            }]
        }
        return Response(data)

# Overdue Trends View
class OverdueTrendsView(APIView):
    def get(self, request):
        # Your logic to gather overdue trends data
        data = {
            'labels': ['Jan', 'Feb', 'Mar'],
            'datasets': [{
                'label': 'Overdue Communications',
                'data': [5, 10, 3]
            }]
        }
        return Response(data)

# Real-Time Activity Log View
class ActivityLogView(APIView):
    def get(self, request):
        # Your logic to gather real-time activity log data
        data = [
            {'date': '2025-01-01', 'user': 'Phani', 'action': 'Sent an email to Company'},
            {'date': '2025-01-02', 'user': 'Bary', 'action': 'Called Tesla'},
        ]
        return Response(data)
