from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TrackedSiteCreateSerializer
from .utils.api_key_validator import validate_api_key
from .services.visitor_engine import get_or_create_visitor
from .services.session_engine import get_or_create_session, close_session
from .models import pageview, session


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
                "message": "Website created",
                "site_id": str(site.site_id),
                "api_key": site.api_key,
                "tracking_script": tracking_script
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
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
                "message": "API key valid",
                "site_name": site.site_name
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
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
                    "message": "visitor_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            visitor = get_or_create_visitor(site, visitor_id)
            
            track_session = get_or_create_session(site, visitor, request)
            


            # Log Page View
            page_url = request.data.get('page_url')
            if not page_url:
                return Response({
                    "status": False,
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
            
            return Response({
                "status": True,
                "message": "Page view logged",
                "session_id": str(track_session.id)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)





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
            
            # Close last open page view
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
                    "message": "Session closed",
                    "duration": track_session.duration
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": "No active session found"
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
