import requests
from abc import ABC, abstractmethod

from ..DataManager.db_manager import DbManager

class BaseManager(ABC):

    def __init__(self, url, update_func) -> None:
        
        self._data = []
        self.url = url
        self.db_manager = DbManager()
        self.update_func = update_func
        
    @property
    def data(self) -> list:
        return self._data
    
    @abstractmethod
    def _filter(self, json: dict) -> None:
        pass
    
    def _fetch(self):
        response = requests.get(self.url)
        data_json = response.json()
        
        if isinstance(data_json, dict) and len(data_json) > 0:
            self._filter(data_json)
            
    def update(self):
        try:
            self._fetch()
        except Exception as e:
            print(e)
            return None
        
        self.update_func(self.data)