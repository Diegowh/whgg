from django.urls import path, include, re_path

from summoner_profile.apis.backend.views import test_api_client
from summoner_profile.views import ProfileDataView

urlpatterns = [
    
    path('test-api-client/', test_api_client, name='test_api_client'),
    path('<str:server>/<str:summoner_name>/', ProfileDataView.as_view(), name='profile_data'),
    
]