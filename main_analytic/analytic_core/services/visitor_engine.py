from django.utils import timezone
from ..models import Visitor

def get_or_create_visitor(site, visitor_id):
    visitor, created = Visitor.objects.get_or_create(
        site_id=site,
        visitor_id=visitor_id,
        defaults={'site_name': site.site_name}
    )
    
    if not created:
        visitor.site_name = site.site_name
        visitor.last_visit = timezone.now()
        visitor.save()
        
    return visitor
