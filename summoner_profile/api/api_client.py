import os
import time
import requests
from api_throttler import ApiThrottler
from functools import wraps

from .utils import utils as utils
from .utils import exceptions as exc

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
    
    def __init__(self, server, api_key, debug=False) -> None:
        self.api_key = api_key
        self._rl = RateLimiterManager(debug)
        
    def __str__(self):
        return str(self._rl.on(self._platform))
    
    
    def set_server(self, server):
        if server in self.PLATFORMS:
            self.set_platform(server)
        elif server in self.REGIONS:
            self.set_region(server)
        else:
            raise exc.InvalidServer(server, self.PLATFORMS + self.REGIONS)
        
    
    def set_platform(self, platform):
        if platform in self.PLATFORMS:
            self._platform = platform
            self._region = self.PLATFORMS_TO_REGIONS[platform]
        else:
            raise exc.InvalidServer(platform, self.PLATFORMS)
            
    def set_region(self, region):
        if region in self.REGIONS:
            self._platform = None
            self._region = region
        else:
            raise exc.InvalidServer(region, self.REGIONS)
        
    def locked(self, server) -> bool:
        # Checks if at least one limiter is locked
        return self._rl.on(server).locked()
        
    # def request(self, url, params):
    #     self.api_throttler.throttle()
        
    #     try:
    #         response = requests.get(url, params=params)
    #         response.raise_for_status()
    #     except requests.exceptions.RequestException as e:
    #         if response.status_code == 429:
    #             retry_after = int(response.headers.get('Retry-After', 1))
    #             print(f'API rate limit exceeded. Retrying in {retry_after} seconds.')
    #             print("Are you sure ApiThrottler is working?")
    #             time.sleep(retry_after)
                