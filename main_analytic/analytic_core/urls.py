from django.urls import path
from .views import CreateSiteView, TestApiKeyView, CollectStartView, CollectPingView, CollectEndView, OverviewView, CountriesReportView, TopPagesReportView, VisitorsReportView

urlpatterns = [
    path('sites/create/', CreateSiteView.as_view(), name='create-site'),
    path('collect/test/', TestApiKeyView.as_view(), name='test-api-key'),
    path('collect/start/', CollectStartView.as_view(), name='collect-start'),
    path('collect/ping/', CollectPingView.as_view(), name='collect-ping'),
    path('collect/end/', CollectEndView.as_view(), name='collect-end'),
    path('reports/overview/', OverviewView.as_view(), name='overview-report'),
    path('reports/countries/', CountriesReportView.as_view(), name='countries-report'),
    path('reports/top-pages/', TopPagesReportView.as_view(), name='top-pages-report'),
    path('reports/visitors/', VisitorsReportView.as_view(), name='visitors-report'),
]
