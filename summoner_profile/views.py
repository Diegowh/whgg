from rest_framework.views import APIView
from rest_framework.response import Response
from .controllers.request_manager import RequestManager


class SummonerProfileView(APIView):
    
    def get(self, request, summoner_name: str, server: str):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        response_data = request_manager.get()
        
        response = Response(response_data.to_dict())
        return response
