from django.db.models import Avg
from analytic_core.models import Visitor, session, pageview

def overview_report(site_id) -> dict:
    total_visitors = Visitor.objects.filter(site_id=site_id).count()
    
    total_sessions = session.objects.filter(site_id=site_id, is_bot=False).count()
    
    total_pageviews = pageview.objects.filter(
        session_id__site_id=site_id, 
        session_id__is_bot=False
    ).count()
    
    avg_result = session.objects.filter(
        site_id=site_id, 
        is_bot=False, 
        end_time__isnull=False
    ).aggregate(avg_duration=Avg('duration'))
    
    avg_duration = avg_result['avg_duration']
    avg_session_duration = int(avg_duration) if avg_duration is not None else 0
    


    #Bot Sessions Count
    bot_sessions = session.objects.filter(site_id=site_id, is_bot=True).count()
    
    return {
        "status": True,
        "response_code": 200,
        "message": "Overview report generated successfully",
        "data": {
        "site_id": str(site_id),
        "total_visitors": total_visitors,
        "total_sessions": total_sessions,
        "total_pageviews": total_pageviews,
        "avg_session_duration": avg_session_duration,
        "bot_sessions": bot_sessions
        }
    }