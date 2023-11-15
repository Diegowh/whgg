from functools import wraps

import asyncio
import json

from ..apis.riot.utils import utils as utils
from ..apis.riot.utils import exceptions as exc

def ratelimit_platform(func):
    """
    Decorator for rate limiting at platform level.
    It will handle the operations needed by the RateLimiterManager to ensure the rate limiting and change of limits considering the returned header
    """
    
    @wraps(func)
    async def wait_limit(*args, **params):
        rate_limit = args[0]._rl.on(args[0]._platform)
        token = await rate_limit.get_token(func.__name__)
        
        response = await func(*args, **params)
        
        try:
            limits = utils.get_limits(response.headers)
            timestamp = utils.get_timestamp(response.headers)
        except:
            limits = None
            timestamp = utils.get_timestamp(None)
            
        await rate_limit.get_back(func.__name__, token, timestamp, limits)
        
        return response
    
    return wait_limit

def ratelimit_region(func):
    """
    Decorator for rate limiting at region level.
    It will handle the operations needed by the RateLimiterManager to ensure the rate limiting and the change of limits considering the returned header.
    """
    @wraps(func)
    async def wait_limit(*args, **params):
        rate_limit = args[0]._rl.on(args[0]._region)
        token = await rate_limit.get_token(func.__name__)
        
        response = await func(*args, **params)
        
        try:
            limits = utils.get_limits(response.headers)
            timestamp = utils.get_timestamp(response.headers)
        except:
            limits = None
            timestamp = utils.get_timestamp(None)
        
        await rate_limit.get_back(func.__name__, token, timestamp, limits)
        
        return response
        
    return wait_limit

def ratelimit_tournament(func):
    """
    Decorator for rate limiting for tournaments.
    It will handle the operations needed by the RateLimiterManager to ensure the rate limiting and the change of limits considering the returned header.
    """
    @wraps(func)
    async def wait_limit(*args, **params):
        rl = args[0]._rl.on(args[0].TOURNAMENT_REGION)
        token = await rl.get_token(func.__name__)
        
        response = await func(*args, **params)
        
        try:
            limits = utils.get_limits(response.headers)
            timestamp = utils.get_timestamp(response.headers)
        except:
            limits = None
            timestamp = utils.get_timestamp(None)
        
        await rl.get_back(func.__name__, token, timestamp, limits)
        
        return response
        
    return wait_limit


def auto_retry(func):
    """
    Decorator for handling some errors and retrying if needed.
    """
    @wraps(func)
    async def _auto_retry(*args, **params):
        """
        Error handling function for decorator
        """
        if not args[0]._auto_retry:
            return await func(*args, **params)
        else:
            try:
                return await func(*args, **params)
            #Errors that should be retried
            except exc.RateLimit as e:
                if args[0]._debug:
                    print(e)
                    print("Retrying")
                i = e.wait_for()
                while i < 6:
                    await asyncio.sleep(i)
                    try:
                        return await func(*args, **params)
                    except Exception as e2:
                        if args[0]._debug:
                            print(e2)
                    i += 2
                raise e
            except (exc.ServerError, exc.Timeout) as e:
                if args[0]._debug:
                    print(e)
                    print("Retrying")
                i = 1
                while i < 6:
                    await asyncio.sleep(i)
                    try:
                        return await func(*args, **params)
                    except (exc.Timeout, exc.ServerError) as e2:
                
                        pass
                    i += 2
                    if args[0]._debug:
                        print(e2) # type: ignore
                        print("Retrying")
                print("there is no bug")
                raise e
            except (exc.NotFound, exc.BadRequest) as e:
                raise e
            except (exc.Forbidden, exc.Unauthorized,) as e:
                print(e)
                raise SystemExit(0)
            except Exception as e:
                raise e
            
    return _auto_retry

def exceptions(func):
    """
    Translates status code into exceptions
    """

    @wraps(func)
    async def _exceptions(*args, **params):
        
        response = await func(*args, **params)
        
        if response is None:
            raise exc.Timeout
        
        elif response.status == 200:
            return json.loads(await response.text())
        
        elif response.status == 404:
            raise exc.NotFound
            
        elif response.status in [500,502,503,504]:
            raise exc.ServerError
            
        elif response.status == 429:
            raise exc.RateLimit(response.headers)
            
        elif response.status == 403:
            raise exc.Forbidden
            
        elif response.status == 401:
            raise exc.Unauthorized
            
        elif response.status == 400:
            raise exc.BadRequest
            
        elif response.status == 408:
            raise exc.Timeout
            
        else:
            raise Exception("Unidentified error code : "+str(response.status))
    
    return _exceptions