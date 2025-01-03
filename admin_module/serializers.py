from rest_framework import serializers
from .models import Company, CommunicationMethod, Communication
from datetime import datetime
from django.utils.timezone import now

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
        # Try to get the next scheduled communication from the database
        communication = Communication.objects.filter(company=obj, date__gte=now()).order_by('date').first()

        # If no communication is found, return static data
        if communication:
            return {
                "method": communication.method.name,
                "date": communication.date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
                "notes": communication.notes,
                "status": communication.status
            }

        # Static data as fallback if no scheduled communication is found
        static_data = {
            "Apple Inc.": {
                "method": "Email",
                "date": "2025-01-01",
                "notes": "Scheduled email to Apple.",
                "status": "Pending"
            },
            "Google": {
                "method": "Phone Call",
                "date": "2025-01-03",
                "notes": "Scheduled phone call with Google.",
                "status": "Pending"
            },
            "Microsoft": {
                "method": "LinkedIn Post",
                "date": "2025-01-07",
                "notes": "Scheduled LinkedIn post for Microsoft.",
                "status": "Pending"
            },
            "Amazon": {
                "method": "Email",
                "date": "2025-01-08",
                "notes": "Scheduled email to Amazon.",
                "status": "Pending"
            },
            "Tesla": {
                "method": "LinkedIn Post",
                "date": "2025-01-14",
                "notes": "Scheduled LinkedIn post for Tesla.",
                "status": "Pending"
            }
        }

        # Return the static data for the company if no dynamic data is found
        company_name = obj.name
        if company_name in static_data:
            return static_data[company_name]
        
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
