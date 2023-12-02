from functools import wraps

import time
import json

from summoner_profile.utils import utils as utils
from summoner_profile.utils import exceptions as exc

def ratelimit_platform(func):
    """
    Decorator for rate limiting at platform level.
    It will handle the operations needed by the RateLimiterManager to ensure the rate limiting and change of limits considering the returned header
    """
    
    @wraps(func)
    def wait_limit(*args, **params):
        rate_limit = args[0]._rl.on(args[0]._platform)
        token = rate_limit.get_token(func.__name__)
        
        response = func(*args, **params)
        
        try:
            limits = utils.get_limits(response.headers)
            timestamp = utils.get_timestamp(response.headers)
        except:
            limits = None
            timestamp = utils.get_timestamp(None)
            
        rate_limit.get_back(func.__name__, token, timestamp, limits)
        
        return response
    
    return wait_limit

def exceptions(func):
    """
    Translates status code into exceptions
    """

    @wraps(func)
    def _exceptions(*args, **params):
        
        response = func(*args, **params)
        
        if response is None:
            raise exc.Timeout
        
        elif response.status_code == 200:
            return response.json()
        
        elif response.status_code == 404:
            raise exc.NotFound
            
        elif response.status_code in [500,502,503,504]:
            raise exc.ServerError
            
        elif response.status_code == 429:
            raise exc.RateLimit(response.headers)
            
        elif response.status_code == 403:
            raise exc.Forbidden
            
        elif response.status_code == 401:
            raise exc.Unauthorized
            
        elif response.status_code == 400:
            raise exc.BadRequest
            
        elif response.status_code == 408:
            raise exc.Timeout
            
        else:
            raise Exception("Unidentified error code : "+str(response.status_code))
    
    return _exceptions