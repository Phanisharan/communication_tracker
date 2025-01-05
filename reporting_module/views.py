from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Report
from reportlab.pdfgen import canvas
from .serializers import ReportSerializer
import csv

# ViewSet for CRUD operations on the Report model
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# View for downloading a CSV report
def download_csv_report(request):
    try:
        reports = Report.objects.all()
        if not reports.exists():
            return HttpResponse("No reports available to download.", status=404)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports.csv"'

        writer = csv.writer(response)
        writer.writerow(['Company', 'Report Date', 'Summary'])

        for report in reports:
            writer.writerow([report.company.name, report.report_date, report.summary])

        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# View for downloading a PDF report
def download_pdf_report(request):
    try:
        reports = Report.objects.all()
        if not reports.exists():
            return HttpResponse("No reports available to download.", status=404)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Reports Summary")
        y = 780

        for report in reports:
            text = f"Company: {report.company.name}, Date: {report.report_date}, Summary: {report.summary}"
            p.drawString(100, y, text)
            y -= 20

            # Handle page overflow
            if y < 50:
                p.showPage()
                y = 800

        p.save()
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# API View for Communication Frequency
class CommunicationFrequencyView(APIView):
    def get(self, request):
        try:
            # Replace this logic with dynamic data retrieval
            data = {
                'labels': ['LinkedIn Post', 'Email', 'Phone Call'],
                'datasets': [{
                    'label': 'Frequency',
                    'data': [10, 20, 5]  # Example data
                }]
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# API View for Engagement Effectiveness
class EngagementEffectivenessView(APIView):
    def get(self, request):
        try:
            # Replace this logic with dynamic data retrieval
            data = {
                'labels': ['LinkedIn Post', 'Email', 'Phone Call'],
                'datasets': [{
                    'label': 'Effectiveness',
                    'data': [70, 50, 30]  # Example data
                }]
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# API View for Overdue Trends
class OverdueTrendsView(APIView):
    def get(self, request):
        try:
            # Replace this logic with dynamic data retrieval
            data = {
                'labels': ['Jan', 'Feb', 'Mar'],
                'datasets': [{
                    'label': 'Overdue Communications',
                    'data': [5, 10, 3]  # Example data
                }]
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# API View for Real-Time Activity Log
class ActivityLogView(APIView):
    def get(self, request):
        try:
            # Replace this logic with dynamic data retrieval
            data = [
                {'date': '2025-01-01', 'user': 'Phani', 'action': 'Sent an email to Company'},
                {'date': '2025-01-02', 'user': 'Bary', 'action': 'Called Tesla'},
            ]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
