from rest_framework import serializers
from .models import VisitorAnalytics

class VisitorAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorAnalytics
        fields = '__all__'
