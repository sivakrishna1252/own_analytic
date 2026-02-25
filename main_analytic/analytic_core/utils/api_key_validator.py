from rest_framework.exceptions import ValidationError
from ..models import TrackedSite

def validate_api_key(api_key):
    if not api_key:
        raise ValidationError({"api_key": "API key is required."})
    try:
        site = TrackedSite.objects.get(api_key=api_key)
        return site
    except TrackedSite.DoesNotExist:
        raise ValidationError({"api_key": "Invalid API key."})
