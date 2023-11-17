from rest_framework.views import APIView
from rest_framework.response import Response
from controllers.request_manager import RequestManager


class BaseDataView(APIView):
    data_key = ""
    
    def get(self, request, summoner_name: str, server: str, format=None):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.requested_data[self.data_key]
        return Response(data)

class SummonerDataView(APIView):
    
    def get(self, request, summoner_name: str, server: str, format=None):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.requested_data["summoner_info"]
        return Response(data)
        

class RankedDataView(APIView):
    
    def get(self, request, summoner_name: str, server: str, format=None):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.requested_data["ranked_data"]
        return Response(data)
    
    
class ChampionStatView(APIView):
    
    def get(self, request, summoner_name: str, server: str, format=None):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.requested_data["champion_stats"]
        return Response(data)
    
class MatchHistoryView(APIView):
    
    def get(self, request, summoner_name: str, server: str, format=None):
        
        request_manager = RequestManager(summoner_name=summoner_name, server=server)
        data = request_manager.requested_data["match_history"]
        return Response(data)