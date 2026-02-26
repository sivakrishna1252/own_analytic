"""
URL configuration for main_analytic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.conf.urls.static import static
import os

def home(request):
    return HttpResponse("winter is coming")

def serve_tracker(request):
    tracker_path = os.path.join(settings.BASE_DIR, 'static', 'tracker.js')
    if os.path.exists(tracker_path):
        return FileResponse(open(tracker_path, 'rb'), content_type='application/javascript')
    return HttpResponse("// tracker.js not found", status=404)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include('analytic_core.urls')),
    path('tracker.js', serve_tracker, name='serve-tracker'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else os.path.join(settings.BASE_DIR, 'static'))
