import os
import time
import requests
from api_throttler import ApiThrottler

class ApiClient:
    def __init__(self) -> None:
        self.api_key = os.environ['RIOT_API_KEY']
        self.api_throttler = ApiThrottler()
        
    def request(self, url, params):
        self.api_throttler.throttle()
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f'API rate limit exceeded. Retrying in {retry_after} seconds.')
                print("Are you sure ApiThrottler is working?")
                time.sleep(retry_after)
                