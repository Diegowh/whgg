from datetime import datetime
import time


from .data_manager import DataManager
from summoner_profile.utils.dataclasses import RequestData, ResponseData



class RequestManager:

    def __init__(self, summoner_name: str, server: str) -> None: #TODO Cambiar esto para que obtenga un Riot ID en vez de un Summoner Name
        
        self._summoner_name = summoner_name
        self._server = server
        
        self._request_data: RequestData = RequestData(summoner_name=self.summoner_name, server=self.server)
        
        
        # Inicializa el DataManager
        self.data_manager = DataManager(request=self.request_data)
        
    # Properties
    @property
    def summoner_name(self):
        return self._summoner_name
    
    @property
    def server(self):
        return self._server
        
    @property
    def request_data(self):
        return self._request_data
    
    def get(self) -> ResponseData:
        return self.data_manager.get_requested_data()