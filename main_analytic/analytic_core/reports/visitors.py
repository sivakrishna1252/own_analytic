from django.db.models import Count, Sum, Q
from analytic_core.models import Visitor, session, TrackedSite

def get_visitors_report(site) -> dict:
    visitors_qs = Visitor.objects.filter(
        site_id=site,
        session__is_bot=False
    ).distinct().annotate(
        calc_total_sessions=Count('session', filter=Q(session__is_bot=False), distinct=True),
        calc_total_pageviews=Count('session__pageview', filter=Q(session__is_bot=False)),
        calc_total_time_spent=Sum('session__duration', filter=Q(session__is_bot=False, session__end_time__isnull=False))
    ).order_by('-last_visit')

    visitors_list = []
    for v in visitors_qs:
        visitors_list.append({
            "visitor_id": v.visitor_id,
            "first_visit": v.first_visit.isoformat(),
            "last_visit": v.last_visit.isoformat(),
            "total_sessions": v.calc_total_sessions,
            "total_pageviews": v.calc_total_pageviews,
            "total_time_spent": v.calc_total_time_spent or 0,
            "is_returning": v.calc_total_sessions > 1
        })

    return {
        "status": True,
        "response_code": 200,
        "message": "Visitors report generated successfully",
        "data": {
            "site": {
                "site_id": str(site.site_id),
                "site_name": site.site_name
            },
            "total_visitors": len(visitors_list),
            "visitors": visitors_list
        }
    }
