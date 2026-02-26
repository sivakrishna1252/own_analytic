from datetime import timedelta
from django.utils import timezone
from ..models import session
from .geoip_service import get_country_from_ip
from .bot_detection import is_bot_request

def get_or_create_session(site, visitor, request):
    now = timezone.now()
    
    active_session = session.objects.filter(
        site_id=site,
        visitor_id=visitor,
        end_time__isnull=True
    ).first()
    

    #30min-session
    if active_session:
        if active_session.last_activity and (now - active_session.last_activity) > timedelta(minutes=30):
            active_session.end_time = active_session.last_activity
            delta = active_session.last_activity - active_session.start_time
            active_session.duration = int(delta.total_seconds())
            active_session.save()
        else:
            return active_session

   
        
    # Create new session
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '').strip()



     #detect country   
    country = get_country_from_ip(ip)
        
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    


    # detect bot
    is_bot_flag = is_bot_request(user_agent)
    
    new_session = session.objects.create(
        site_id=site,
        visitor_id=visitor,
        ip_address=ip,
        country=country,
        user_agent=user_agent,
        last_activity=now,
        is_bot=is_bot_flag
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
