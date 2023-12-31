from django.urls import path, include, re_path
from .views import SummonerProfileView

urlpatterns = [
    
    path('<str:server>/<str:game_name>-<str:tagline>/', SummonerProfileView.as_view(), name='summoner_profile'),
    
]