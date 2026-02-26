from django.db.models import Count
from analytic_core.models import pageview

def top_pages_report(site_id) -> dict:
    total_pageviews = pageview.objects.filter(
        session_id__site_id=site_id, 
        session_id__is_bot=False
    ).count()
    
    pages_list = []
    
    if total_pageviews > 0:
        pages_data = pageview.objects.filter(
            session_id__site_id=site_id, 
            session_id__is_bot=False
        ).values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')
        
        for item in pages_data:
            pages_list.append({
                "page_url": item['page_url'],
                "views": item['views']
            })

    return {
        "status": True,
        "response_code": 200,
        "message": "Top pages report generated successfully",
        "data": {
            "site_id": str(site_id),
            "total_pageviews": total_pageviews,
            "pages": pages_list
        }
    }
