import requests
from abc import ABC, abstractmethod

from ..DataManager.db_manager import DbManager

class BaseManager(ABC):

    def __init__(self, url) -> None:
        
        self._data = []
        self.url = url
        
    @property
    def data(self) -> list:
        return self._data
    
    @abstractmethod
    def _filter(self, json: dict) -> None:
        pass
        
    
    def _fetch(self):
        try:
            response = requests.get(self.url)
            data_json = response.json()
        
            if isinstance(data_json, dict) and len(data_json) > 0:
                self._filter(data_json)
                
        except Exception as e:
            print(e)
            return None
    
    def is_updated(self) -> bool:
        self._fetch()
        return True