import requests
from abc import ABC, abstractmethod


class BaseManager(ABC):

    def __init__(self, url) -> None:

        self._data = []
        self.url = url

    @property
    def data(self) -> list:
        return self._data

    @abstractmethod
    def _filter(self, json: dict):
        pass

    def fetch(self):
        try:
            response = requests.get(self.url)
            data_json = response.json()

            if isinstance(data_json, dict) and len(data_json) > 0:
                print("Data fetched successfully")
                self._filter(data_json)

                return self.data

        except Exception as e:
            print(e)
            return None
