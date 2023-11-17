from django.contrib import admin
from django.urls import path, include

from summoner_profile.apis.backend.views import test_api_client
from summoner_profile.views import SummonerDataView


urlpatterns = [
    
    path('test-api-client/', test_api_client, name='test_api_client'),
    path('api/<str:server>/<str:summoner_name>/', SummonerDataView.as_view()),
    
]