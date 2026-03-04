from django.db.models import Count, Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import TrackedSite, pageview, session

class AnalyticsDashboardAPI(APIView):
    def get(self, request):
        site_id = request.query_params.get('site_id')
        search_query = request.query_params.get('search', '')


        #pagination (defalut 1 page and limit 10)
        page_number = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('allow', request.query_params.get('per_page', 10)))

        if not site_id:
            return Response({
                "status": False,
                "message": "site_id query parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            site = TrackedSite.objects.get(site_id=site_id)
        except (TrackedSite.DoesNotExist, ValueError):
            return Response({
                "status": False,
                "message": "Invalid or missing site"
            }, status=status.HTTP_404_NOT_FOUND)

        from django.core.paginator import EmptyPage, PageNotAnInteger



        # 1. Top Pages with Search & Pagination
        pages_qs = pageview.objects.filter(
            site_id=site,
            session_id__is_bot=False
        )
        if search_query:
            pages_qs = pages_qs.filter(page_url__icontains=search_query)
        
        pages_data = pages_qs.values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')
        
        pages_paginator = Paginator(pages_data, per_page)
        try:
            curr_pages_page = pages_paginator.page(page_number)
            pages_results = [{
                "page_url": item['page_url'],
                "views": item['views']
            } for item in curr_pages_page]
        except (EmptyPage, PageNotAnInteger):
            pages_results = []




        # 2. Countries with Search & Pagination
        countries_qs = session.objects.filter(
            site_id=site,
            is_bot=False
        )
        if search_query:
            countries_qs = countries_qs.filter(country__icontains=search_query)

        countries_data = countries_qs.values('country').annotate(
            sessions=Count('id'),
            visitors=Count('visitor_id', distinct=True)
        ).order_by('-sessions')

        countries_paginator = Paginator(countries_data, per_page)
        try:
            curr_countries_page = countries_paginator.page(page_number)
            countries_results = [{
                "country": item['country'] if item['country'] else "Unknown",
                "visitors": item['visitors'],
                "sessions": item['sessions']
            } for item in curr_countries_page]
        except (EmptyPage, PageNotAnInteger):
            countries_results = []




        # 3. Visitors with Search & Pagination
        base_visitors_qs = session.objects.filter(
            site_id=site,
            is_bot=False
        )
        
        if search_query:
            base_visitors_qs = base_visitors_qs.filter(
                Q(visitor_id__visitor_id__icontains=search_query) | 
                Q(country__icontains=search_query) | 
                Q(ip_address__icontains=search_query)
            )

        visitors_data = base_visitors_qs.values('visitor_id__visitor_id').annotate(
            total_sessions=Count('id', distinct=True),
            total_pageviews=Count('pageview')
        ).order_by('-total_sessions')

        visitors_paginator = Paginator(visitors_data, per_page)
        try:
            curr_visitors_page = visitors_paginator.page(page_number)
            visitors_results = [{
                "visitor_id": item['visitor_id__visitor_id'],
                "total_sessions": item['total_sessions'],
                "total_page_hits": item['total_pageviews']
            } for item in curr_visitors_page]
        except (EmptyPage, PageNotAnInteger):
            visitors_results = []

        return Response({
            "status": True,
            "site": {
                "site_id": str(site.site_id),
                "site_name": site.site_name
            },
            "data": {
                "top_pages": pages_results,
                "countries": countries_results,
                "visitors": visitors_results
            },
            "page": page_number,
            "limit": per_page,
            # "total_pages": pages_paginator.num_pages,
            "total_items": pages_paginator.count,
        }, status=status.HTTP_200_OK)
