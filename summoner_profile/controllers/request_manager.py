from .data_manager import DataManager
from summoner_profile.utils.dataclasses import RequestData, ResponseData


class RequestManager:

    """
    Clase encargada de gestionar las peticiones del front-end y devolver los datos necesarios para la vista.
    """

    def __init__(

        self,
        game_name: str,
        tagline: str,
        server: str

    ) -> None:

        self._game_name = game_name
        self._tagline = tagline
        self._server = server

        self._request_data: RequestData = RequestData(
            game_name=self.game_name, tagline=self.tagline, server=self.server)

        # Inicializa el DataManager
        self.data_manager = DataManager(request=self.request_data)

    # Properties
    @property
    def game_name(self):
        return self._game_name

    @property
    def tagline(self):
        return self._tagline

    @property
    def server(self):
        return self._server

    @property
    def request_data(self):
        return self._request_data

    def get(self) -> ResponseData:
        """Devuelve los datos requeridos.
        """
        return self.data_manager.get_response_data()
