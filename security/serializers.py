from rest_framework import serializers
from .models import ThreatAlert

class ThreatAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatAlert
        fields = '__all__'
