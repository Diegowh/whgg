import os
import time
import requests
import ssl
import certifi
import json
import asyncio
import aiohttp
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
    
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
    
    def __init__(self, server, api_key, auto_retry = False, requests_logging_function = None, debug=False) -> None:
        self._key = api_key
        self._rl = RateLimiterManager(debug)
        
        self.set_server(server)
        
        self._requests_logging_function = requests_logging_function
        
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
                    i = e.waitFor()
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
                            print(e2)
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
    
    async def fetch(self, url, method="GET", data=None):
        """
        Attaches the api_key to the header and returns a request response of the given url.
        """
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-Riot-Token": self._key
            }
            
                
            try:
                if method == "GET":
                    response = await session.request("GET", url, headers=headers, ssl=self.SSL_CONTEXT)
                else:
                    response = await session.request(method, url, headers=headers, data=json.dumps(data), ssl=self.SSL_CONTEXT)
            
            # In case of timeout
            except Exception as e:
                print(e)
                return None
            
            # If a logging function is passed, send it url status code and headers
            if self._requests_logging_function:
                self._requests_logging_function(url, response.status, response.headers)
            
            await response.text()
            return response
    
    # Champion Mastery
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_champion_masteries(self, summoner_id: str):
        """
        :param string summoner_id: summoner_id of the player
        
        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getAllChampionMasteries
        """
        return await self.fetch((self.BASE_URL_LOL + "champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}").format(server=self._platform, summoner_id=summoner_id))
    
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_champion_masteries_by_champion_id(self, summoner_id, champion_id):
        """
        :param string summoner_id: summoner_id of the player
        :param int championId: id of the champion

        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMastery
        """
        return await self.fetch((self.BASE_URL_LOL + "champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}").format(server=self._platform, summonerId=summoner_id, championId=champion_id))

    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_champion_masteries_score(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player
        
        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMasteryScore
        """
        return await self.fetch((self.BASE_URL_LOL + "champion-mastery/v4/scores/by-summoner/{summoner_id}").format(server=self._platform, summoner_id=summoner_id))
    
    # Champion rotations
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_champion_rotations(self):
        """
        Returns the result of https://developer.riotgames.com/api-methods/#champion-v3/GET_getChampionInfo
        """
        return await self.fetch((self.BASE_URL_LOL + "platform/v3/champion-rotations").format(server=self._platform))
    
    # League
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_league_by_id(self, league_id):
        """
        :param string league_id: id of the league
        
        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueById
        """
        return await self.fetch((self.BASE_URL_LOL + "league/v4/leagues/{league_id}").format(server=self._platform, league_id=league_id))
    
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_league_pages(self, queue="RANKED_SOLO_5X5", tier="DIAMOND", division="I", page=1):
        """
        :param string queue: queue to get the page of
        :param string tier: tier to get the page of
        :param string division: division to get the page of
        :param int page: page to get
        
        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueEntriesForSummoner
        """
        return await self.fetch((self.BASE_URL_LOL + "league/v4/entries/{queue}/{tier}/{division}?page={page}").format(server=self._platform, queue=queue, tier=tier, division=division, page=page))
    
    @auto_retry
    @exceptions
    @ratelimit_platform
    async def get_challenger_league(self, queue="RANKED_SOLO_5x5"):
        """
        :param string queue: queue to get the challenger league of
            Values accepted : 
             * RANKED_SOLO_5x5 *(default)*
             * RANKED_FLEX_SR
        
        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getChallengerLeague
        """
        return await self.fetch((self.BASE_URL_LOL + "league/v4/challengerleagues/by-queue/{queue}").format(server=self._platform, queue=queue))