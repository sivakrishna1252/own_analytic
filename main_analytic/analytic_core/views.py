from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TrackedSiteCreateSerializer
from .utils.api_key_validator import validate_api_key
from .services.visitor_engine import get_or_create_visitor
from .services.session_engine import get_or_create_session, close_session
from .models import pageview, session, TrackedSite
from .reports.overview_report import overview_report
from .reports.countries import countries_report
from .reports.top_pages import top_pages

#siteapi
class CreateSiteView(APIView):
    def post(self, request):
        serializer = TrackedSiteCreateSerializer(data=request.data)
        if serializer.is_valid():
            site = serializer.save()
            domain = request.build_absolute_uri('/')[:-1]
            tracking_script = f'<script async src="{domain}/tracker.js" data-api-key="{site.api_key}"></script>'
            return Response({
                "status": True,
                "response_code": 201,
                "message": "Website created",
                "site_id": str(site.site_id),
                "api_key": site.api_key,
                "tracking_script": tracking_script
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "response_code": 400,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




#testapi (api key validation)
class TestApiKeyView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        try:
            site = validate_api_key(api_key)
            return Response({
                "status": True,
                "response_code": 200,
                "message": "API key valid",
                "site_name": site.site_name
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "response_code": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)






#collectapi (session processing)
class CollectStartView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        visitor_id = request.data.get('visitor_id')
        
        try:
            site = validate_api_key(api_key)
            
            if not visitor_id:
                return Response({
                    "status": False,
                    "response_code": 400,
                    "message": "visitor_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            visitor = get_or_create_visitor(site, visitor_id)
            
            track_session = get_or_create_session(site, visitor, request)
            


            # Log Page View
            page_url = request.data.get('page_url')
            if not page_url:
                return Response({
                    "status": False,
                    "response_code": 400,
                    "message": "page_url is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            now = timezone.now()

            previous_pageview = pageview.objects.filter(
                session_id=track_session,
                end_time__isnull=True
            ).last()
            
            if previous_pageview:
                previous_pageview.end_time = now
                delta = now - previous_pageview.timestamp
                previous_pageview.duration = int(delta.total_seconds())
                previous_pageview.save()


           
                
            # Create new PageView
            pageview.objects.create(
                session_id=track_session,
                page_url=page_url
            )
            
            # Update session last activity
            track_session.last_activity = now
            track_session.save()
            
            return Response({
                "status": True,
                "response_code": 200,
                "message": "Page view logged",
                "session_id": str(track_session.id)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "response_code": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


#ping_api
class CollectPingView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        visitor_id = request.data.get('visitor_id')
        
        try:
            site = validate_api_key(api_key)
            
            if not visitor_id:
                return Response({
                    "status": False,
                    "response_code": 400,
                    "message": "visitor_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            visitor = get_or_create_visitor(site, visitor_id)
            
            active_session = session.objects.filter(
                site_id=site,
                visitor_id=visitor,
                end_time__isnull=True
            ).first()
            
            if not active_session:
                return Response({
                    "status": True,
                    "response_code": 200,
                    "message": "Ignored: No active session"
                }, status=status.HTTP_200_OK)
                
            active_session.last_activity = timezone.now()
            active_session.save(update_fields=['last_activity'])
            
            return Response({
                "status": True,
                "response_code": 200,
                "message": "Ping processed successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "response_code": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)





#end_api
class CollectEndView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        visitor_id = request.data.get('visitor_id')
        
        try:
            site = validate_api_key(api_key)
            
            if not visitor_id:
                return Response({
                    "status": False,
                    "message": "visitor_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            visitor = get_or_create_visitor(site, visitor_id)
            
            active_session = session.objects.filter(
                site_id=site,
                visitor_id=visitor,
                end_time__isnull=True
            ).first()
            
            if active_session:
                last_pageview = pageview.objects.filter(
                    session_id=active_session,
                    end_time__isnull=True
                ).last()
                
                if last_pageview:
                    now = timezone.now()
                    last_pageview.end_time = now
                    delta = now - last_pageview.timestamp
                    last_pageview.duration = int(delta.total_seconds())
                    last_pageview.save()
            
            track_session = close_session(site, visitor)
            
            if track_session:
                return Response({
                    "status": True,
                    "response_code": 200,
                    "message": "Session closed",
                    "duration": track_session.duration
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "response_code": 404,
                    "message": "No active session found"
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({
                "status": False,
                "response_code": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)





#all overviews
class OverviewView(APIView):
    def get(self, request):
        site_id = request.query_params.get('site_id')
        
        if not site_id:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "site_id query parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            site = TrackedSite.objects.get(site_id=site_id)
        except TrackedSite.DoesNotExist:
            return Response({
                "status": False,
                "response_code": 404,
                "message": f"Site with id {site_id} not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ValueError:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "Invalid site_id format"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = overview_report(site.site_id)
        
        return Response(data, status=status.HTTP_200_OK)




#countries overview
class CountriesReportView(APIView):
    def get(self, request):
        site_id = request.query_params.get('site_id')
        
        if not site_id:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "site_id query parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            site = TrackedSite.objects.get(site_id=site_id)
        except TrackedSite.DoesNotExist:
            return Response({
                "status": False,
                "response_code": 404,
                "message": f"Site with id {site_id} not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ValueError:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "Invalid site_id format"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = countries_report(site.site_id)
        
        return Response(data, status=status.HTTP_200_OK)


# top pages overview
class TopPagesReportView(APIView):
    def get(self, request):
        site_id = request.query_params.get('site_id')
        
        if not site_id:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "site_id query parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            site = TrackedSite.objects.get(site_id=site_id)
        except TrackedSite.DoesNotExist:
            return Response({
                "status": False,
                "response_code": 404,
                "message": f"Site with id {site_id} not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ValueError:
            return Response({
                "status": False,
                "response_code": 400,
                "message": "Invalid site_id format"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
        data = top_pages(site.site_id)
        
        return Response(data, status=status.HTTP_200_OK)
