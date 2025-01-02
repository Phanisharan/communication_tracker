from django.shortcuts import render
from rest_framework import viewsets
from django.utils import timezone
from .models import Company, CommunicationMethod, Communication
from .serializers import CompanySerializer, CommunicationMethodSerializer, CommunicationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CommunicationMethodViewSet(viewsets.ModelViewSet):
    queryset = CommunicationMethod.objects.all()
    serializer_class = CommunicationMethodSerializer

class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        overdue = self.request.query_params.get('overdue', None)
        due_today = self.request.query_params.get('due-today', None)
        if overdue is not None:
            queryset = queryset.filter(date__lt=timezone.now().date(), status='scheduled')
        if due_today is not None:
            queryset = queryset.filter(date=timezone.now().date(),  status='scheduled')
        return queryset


    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue_communications(self, request):
        overdue_communications = self.get_queryset().filter(status='overdue')
        serializer = self.get_serializer(overdue_communications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='due-today')
    def due_today_communications(self, request):
        today = date.today()
        due_today = self.get_queryset().filter(due_date__date=today)
        serializer = self.get_serializer(due_today, many=True)
        return Response(serializer.data)





