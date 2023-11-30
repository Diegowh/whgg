from django.urls import path, include, re_path
from .views import SummonerProfileView

urlpatterns = [
    
    path('<str:server>/<str:summoner_name>/', SummonerProfileView.as_view()),
    
]