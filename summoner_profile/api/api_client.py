import os
import time
import requests
from api_throttler import ApiThrottler

from .RateLimit.rate_limiter_manager import RateLimiterManager

class ApiClient:
    
    BASE_URL = "https://{server}.api.riotgames.com/"
    BASE_URL_LOL = BASE_URL + "lol/"
    BASE_URL_TFT = BASE_URL + "tft/"
    BASE_URL_VAL = BASE_URL + "val/"
    BASE_URL_LOR = BASE_URL + "lor/"
    BASE_URL_RIOT = BASE_URL + "riot/"
    
    PLATFORMS = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","tr1","ru"]
    REGIONS = ["americas","asia","europe", "esports","ap","br","eu","kr","latam","na"]
    PLATFORMS_TO_REGIONS = {"br1":"americas","eun1":"europe","euw1":"europe","jp1":"asia","kr":"asia","la1":"americas","la2":"americas","na1":"americas","oc1":"americas","tr1":"europe","ru":"europe"}
    TOURNAMENT_REGIONS = "americas"
    
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
                