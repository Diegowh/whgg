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
    data_key = "summoner_data"

class RankedDataView(APIView):
    data_key = "ranked_data"
    
    
class ChampionStatView(APIView):
    data_key = "champion_stats"

    
class MatchHistoryView(APIView):
    data_key = "match_history"
