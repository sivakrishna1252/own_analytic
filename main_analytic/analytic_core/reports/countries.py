from django.db.models import Count
from analytic_core.models import session

def countries_report(site_id) -> dict:
    total_sessions = session.objects.filter(site_id=site_id, is_bot=False).count()
    
    countries_list = []
    
    if total_sessions > 0:
        country_data = session.objects.filter(
            site_id=site_id, 
            is_bot=False
        ).values('country').annotate(
            sessions=Count('id')
        ).order_by('-sessions')
        
        for item in country_data:
            country_name = item['country'] if item['country'] else "Unknown"
            sessions_count = item['sessions']
            
            percentage = round((sessions_count / total_sessions) * 100, 2)
            
            countries_list.append({
                "country": country_name,
                "sessions": sessions_count,
                "percentage": percentage
            })




    # Return
    return {
        "status": True,
        "response_code": 200,
        "message": "Countries report generated successfully",
        "data": {
            "site_id": str(site_id),
            "total_sessions": total_sessions,
            "countries": countries_list
        }
    }








    #calculation work like this 
    # total sessions = 100
    # country sessions = 50
    # percentage = (50 / 100) * 100 = 50