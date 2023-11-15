from datetime import datetime
import dotenv
import os
import time

from asgiref.sync import async_to_sync

from .db_manager import DbManager

from .data_formatter import DataFormatter

from ..apis.riot.utils.dataclasses import (
    
    SummonerData,
    SoloqData,
    FlexData,
    RankedData,
    ChampionStatsData,
    
)

from .api_client import ApiClient
from ..apis.riot.utils.exceptions import RiotApiKeyNotFound
from ..apis.riot.utils.utils import hours_to_seconds
from ..models.summoner import Summoner


class RequestManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    def __init__(self, summoner_name: str, server: str) -> None:
        
        self._requested_data = {}
        
        # Summoner requested attributes
        self.summoner_name = summoner_name
        self.server = server
        
        # Get ApiKey from .env 
        try:
            dotenv.load_dotenv()
            
            api_key = os.getenv("RIOT_API_KEY")
            
            if api_key is None:
                raise RiotApiKeyNotFound()
        
        except EnvironmentError:
            raise RiotApiKeyNotFound()
        
        # Instantiate ApiClient to manage requests to Riot API
        self.api_client = ApiClient(server=self.server, api_key=api_key, debug=True)
        
        
        # To avoid repetitive requests for the IDs
        self.summoner_info = async_to_sync(self.fetch_summoner)() # Always request summoner info based on summoner name to Riot API
        self._puuid: str = self.summoner_info["puuid"]
        self._id: str = self.summoner_info["id"]
        
        # Create DbManager instance
        self.db_manager = DbManager(puuid=self._puuid)
        
        # Create DataFormatter instance
        self.data_formatter = DataFormatter()
        
    
    @property
    def requested_data(self):
        return self._requested_data
    
    @requested_data.setter
    def requested_data(self, new_data):
        self._requested_data = new_data
    
    
    def fetch_requested_data(self): #TODO Refactorizar este metodo para que esta funcionalidad se haga en la clase DataFormatter. Esta clase debe enviar una peticion de los datos ya formateados a la base de datos mediante el DataFormatter.
        
        # If the summoner puuid is already in the database
        if self.db_manager.is_puuid_in_database():
            
            # Check how much time has been since last update
            now = int(time.time())
            last_update = self.db_manager.last_update()
            
            if (now - last_update) > self.SECONDS_BEFORE_UPDATING_DATABASE:
                
                # Request data from Riot API using ApiClient
                summoner_request = async_to_sync(self.fetch_summoner)()
                ranked_stats_request = async_to_sync(self.fetch_ranked_stats)()
                champion_stats_request = ...
                
                # Send the data to DbManager to update the database
                pass
            
            else:
                # Return summoners data from the database without an update
                pass
        
        # If the summoner puuid is not in the database
        else:
            # Update the database
            pass
    
    # Request data from Riot API
    async def fetch_summoner(self):
        '''
        Returns structured data ready to send it to Summoner model
        '''
        response = await self.api_client.get_summoner_by_name()
        
        summoner = {
            "puuid": response["puuid"],
            "id": response["id"],
            "name": response["name"],
            "server": self.server,
            "icon_id": response["profileIconId"],
            "summoner_level": response["summonerLevel"],
            "last_update": response["revisionDate"]
            
        }
        
        return summoner
    
    async def fetch_ranked_stats(self) -> dict:
        '''
        Returns structured data ready to send it to RankedStats model
        '''
        response = await self.api_client.get_league_by_summoner(summoner_id=self._id)
        
        soloq_stats = flex_stats = None
        
        for queue_stats in response:
            
            if queue_stats["queueType"] == "RANKED_SOLO_5x5":
                
                soloq_stats = {
                    "queue_type": queue_stats["queueType"],
                    "tier": queue_stats["tier"],
                    "rank": queue_stats["rank"],
                    "league_points": queue_stats["leaguePoints"],
                    "wins": queue_stats["wins"],
                    "losses": queue_stats["losses"],
                    "winrate": int(queue_stats["wins"] / (queue_stats["wins"] + queue_stats["losses"]) * 100)
                }
            
            if queue_stats["queueType"] == "RANKED_FLEX_SR":
                
                flex_stats = {
                    "queue_type": queue_stats["queueType"],
                    "tier": queue_stats["tier"],
                    "rank": queue_stats["rank"],
                    "league_points": queue_stats["leaguePoints"],
                    "wins": queue_stats["wins"],
                    "losses": queue_stats["losses"],
                    "winrate": int(queue_stats["wins"] / (queue_stats["wins"] + queue_stats["losses"]) * 100)
                }
        
        return {"soloq": soloq_stats, "flex": flex_stats}