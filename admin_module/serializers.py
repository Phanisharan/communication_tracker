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
        communications = Communication.objects.filter(company=obj).order_by('-date')[:5]
        return CommunicationSerializer(communications, many=True).data

    def get_nextScheduledCommunication(self, obj):
        communication = Communication.objects.filter(company=obj, date__gte=datetime.today()).order_by('date').first()
        if communication:
            return CommunicationSerializer(communication).data
        return None


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
