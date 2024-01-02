from rest_framework.views import APIView
from rest_framework.response import Response
from .controllers.request_manager import RequestManager


class SummonerProfileView(APIView):

    def get(self, request, game_name: str, tagline: str, server: str):

        request_manager = RequestManager(
            game_name=game_name,
            tagline=tagline,
            server=server)
        response_data = request_manager.get()

        response = Response(response_data.to_dict())
        return response
