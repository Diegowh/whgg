import os
import requests
from api_throttler import ApiThrottler

class ApiClient:
    def __init__(self) -> None:
        self.api_key = os.environ['RIOT_API_KEY']
        
    def request(self, url, params):
        api_throttler = ApiThrottler()