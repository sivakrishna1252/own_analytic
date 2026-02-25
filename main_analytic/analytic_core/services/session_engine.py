from django.utils import timezone
from ..models import session

def get_or_create_session(site, visitor, request):
    # Check for active session
    active_session = session.objects.filter(
        site_id=site,
        visitor_id=visitor,
        end_time__isnull=True
    ).first()
    
    if active_session:
        return active_session

   
        
    # Create new session
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    new_session = session.objects.create(
        site_id=site,
        visitor_id=visitor,
        ip_address=ip,
        user_agent=user_agent
    )
    
    return new_session

def close_session(site, visitor):
 
    active_session = session.objects.filter(
        site_id=site,
        visitor_id=visitor,
        end_time__isnull=True
    ).first()
    
    if active_session:
        now = timezone.now()
        active_session.end_time = now
        

        # Calculate duration in seconds
        delta = now - active_session.start_time
        active_session.duration = int(delta.total_seconds())
        
        active_session.save()
        return active_session
    
    return None
