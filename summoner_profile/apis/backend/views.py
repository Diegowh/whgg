from rest_framework.decorators import api_view
from rest_framework.response import Response

from summoner_profile.controllers.request_manager import RequestManager

@api_view(["GET"])
def get_response(request):
    summoner_name = request.GET["summoner_name"]
    server = request.GET["server"]
    
    request_manager = RequestManager(summoner_name=summoner_name, server=server)
    response_data = request_manager.get()
    
    return Response(response_data.to_dict())