from django.urls import path
from .views import CreateSiteView, TestApiKeyView, CollectStartView, CollectEndView

urlpatterns = [
    path('sites/create/', CreateSiteView.as_view(), name='create-site'),
    path('collect/test/', TestApiKeyView.as_view(), name='test-api-key'),
    path('collect/start/', CollectStartView.as_view(), name='collect-start'),
    path('collect/end/', CollectEndView.as_view(), name='collect-end'),
]
