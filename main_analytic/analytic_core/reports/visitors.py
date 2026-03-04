from django.db.models import Count, Sum, Q
from analytic_core.models import Visitor, session, TrackedSite, pageview

def get_visitors_report(site) -> dict:
    visitors_qs = Visitor.objects.filter(
        site_id=site,
        session__is_bot=False
    ).annotate(
        calc_total_sessions=Count('session', filter=Q(session__is_bot=False), distinct=True),
        calc_total_pageviews=Count('session__pageview', filter=Q(session__is_bot=False)),
    ).order_by('-last_visit')

    visitors_list = []
    for v in visitors_qs:

        # Calculate duration including active sessions
        active_sessions = session.objects.filter(
            visitor_id=v,
            is_bot=False,
            end_time__isnull=True
        )
        
        active_time = 0
        now = timezone.now()
        for s in active_sessions:
            if s.start_time:
                delta = now - s.start_time
                active_time += int(delta.total_seconds())

        completed_time_data = session.objects.filter(
            visitor_id=v,
            is_bot=False,
            end_time__isnull=False
        ).aggregate(total_time=Sum('duration'))
        
        total_time_spent = (completed_time_data['total_time'] or 0) + active_time

        pages_qs = pageview.objects.filter(
            session_id__visitor_id=v,
            session_id__is_bot=False
        ).values('page_url').annotate(visits=Count('id')).order_by('-visits')

        pages_breakdown = [
            {"url": p['page_url'], "visits": p['visits']}
            for p in pages_qs
        ]

        latest_session = session.objects.filter(
            visitor_id=v,
            is_bot=False
        ).order_by('-start_time').first()

        visitors_list.append({
            "id": str(v.id),  # Internal DB ID
            "visitor_id": v.visitor_id, # External LocalStorage ID
            "ip_address": latest_session.ip_address if latest_session else "Unknown",
            "country": latest_session.country if latest_session else "Unknown",
            "browser": latest_session.browser if latest_session else "Unknown",
            "os": latest_session.os if latest_session else "Unknown",
            "device": latest_session.device if latest_session else "Unknown",
            "first_visit": v.first_visit.isoformat(),
            "last_visit": v.last_visit.isoformat(),
            "total_sessions": v.calc_total_sessions,
            "total_pages_hits": v.calc_total_pageviews,
            "unique_pages_visited": len(pages_breakdown),
            "pages_breakdown": pages_breakdown,
            "total_time_spent": total_time_spent,
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
