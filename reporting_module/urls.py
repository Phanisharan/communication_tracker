from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/download/csv', download_csv_report),
    path('reports/download/pdf', download_pdf_report),  
    path('communication-frequency', CommunicationFrequencyView.as_view()),  
    path('engagement-effectiveness', EngagementEffectivenessView.as_view()), 
    path('overdue-trends', OverdueTrendsView.as_view()),  
    path('activity-log', ActivityLogView.as_view()), 
]
