from rest_framework.views import APIView
from rest_framework.response import Response
from summoner_profile.controllers.request_manager import RequestManager


class ProfileDataView(APIView):
    
    def get(self, request, summoner_name: str, server: str):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.get()
        return Response(data)