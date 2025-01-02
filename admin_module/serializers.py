from rest_framework import serializers
from .models import Company, CommunicationMethod, Communication
from datetime import datetime
from django.utils import timezone

class CompanySerializer(serializers.ModelSerializer):
    lastFiveCommunications = serializers.SerializerMethodField()
    nextScheduledCommunication = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'linkedin_profile', 'emails', 'phone_numbers', 'comments', 'communication_periodicity', 'lastFiveCommunications', 'nextScheduledCommunication']

    def get_lastFiveCommunications(self, obj):
        # Get the last 5 communications for the company, ordered by date
        communications = Communication.objects.filter(company=obj).order_by('-date')[:5]
        
        # Add the type field to each communication based on the method
        communications_data = CommunicationSerializer(communications, many=True).data
        for communication in communications_data:
            # Add the communication type based on the method's name
            communication['type'] = communication.get('method', {}).get('name', 'Unknown')  # Default to 'Unknown' if no method
        
        return communications_data


    def get_nextScheduledCommunication(self, obj):
        communication = Communication.objects.filter(company=obj, date__gte=datetime.today()).order_by('date').first()
        if communication:
            return {
                "method": communication.method.name,
                "date": communication.date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
                "notes": communication.notes,
                "status": communication.status
            }
        return None


class CommunicationMethodSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='name')  # Serialize 'name' as 'type'

    class Meta:
        model = CommunicationMethod
        fields = ['id', 'name', 'description', 'sequence', 'is_mandatory', 'type']  


class CommunicationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    method = CommunicationMethodSerializer()
    status = serializers.CharField()

    class Meta:
        model = Communication
        fields = ['id', 'company', 'method', 'date', 'notes', 'status', 'due_date']
