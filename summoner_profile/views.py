from rest_framework.views import APIView
from rest_framework.response import Response
from controllers.request_manager import RequestManager


class ProfileDataView(APIView):
    
    def get(self, request, summoner_name: str, server: str):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.profile_data
        return Response(data)