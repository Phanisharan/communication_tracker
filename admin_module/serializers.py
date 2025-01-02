from rest_framework import serializers
from .models import Company, CommunicationMethod, Communication
from datetime import datetime

class CompanySerializer(serializers.ModelSerializer):
    lastFiveCommunications = serializers.SerializerMethodField()
    nextScheduledCommunication = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'linkedin_profile', 'emails', 'phone_numbers', 'comments', 'communication_periodicity', 'lastFiveCommunications', 'nextScheduledCommunication']


    def get_lastFiveCommunications(self, obj):
        # Return static data for last five communications
        return [
            {"type": "Email", "date": "2025-03-01", "notes": "Initial communication regarding new product launch."},
            {"type": "Phone Call", "date": "2024-01-01", "notes": "Follow-up on marketing partnership discussion."},
            {"type": "LinkedIn Message", "date": "2023-12-10", "notes": "Connection request with senior management."},
            {"type": "Email", "date": "2023-11-15", "notes": "Follow-up email regarding project proposal."},
            {"type": "Phone Call", "date": "2023-11-10", "notes": "Discussion about future collaboration."}
        ]

    def get_nextScheduledCommunication(self, obj):
        # Return static data for next scheduled communication
        return {
            "type": "Email",
            "date": "2025-03-10",
            "notes": "Reminder email for upcoming product launch."
        }


class CommunicationMethodSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='name')  # Serialize 'name' as 'type'

    class Meta:
        model = CommunicationMethod
        fields = ['id', 'name', 'description', 'sequence', 'is_mandatory', 'type']  


class CommunicationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    method = CommunicationMethodSerializer()

    class Meta:
        model = Communication
        fields = '__all__'
