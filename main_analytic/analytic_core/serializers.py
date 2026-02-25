from rest_framework import serializers
from .models import TrackedSite, Visitor, session, pageview

class TrackedSiteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedSite
        fields = ['site_name', 'domain']
    def validate_domain(self, value):
        if not value:
            raise serializers.ValidationError("Domain cannot be empty.")
        return value
