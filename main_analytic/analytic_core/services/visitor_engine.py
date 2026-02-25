from django.utils import timezone
from ..models import Visitor

def get_or_create_visitor(site, visitor_id):
    visitor, created = Visitor.objects.get_or_create(
        site_id=site,
        visitor_id=visitor_id
    )
    
    if not created:
        visitor.last_visit = timezone.now()
        visitor.save()
        
    return visitor
