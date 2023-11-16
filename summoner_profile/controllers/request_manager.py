from datetime import datetime
import re
import dotenv
import os
import time

from asgiref.sync import async_to_sync

from .db_manager import DbManager

from .data_formatter import DataFormatter

from summoner_profile.utils.dataclasses import (
    
    SummonerData,
    RankedStatsData,
    ChampionStatsData,
    SummonerMatchData,
    ParticipantData,
    
)

from .api_client import ApiClient
from summoner_profile.utils.exceptions import RiotApiKeyNotFound
from summoner_profile.utils.utils import hours_to_seconds
from summoner_profile.utils.env_loader import EnvLoader


class RequestManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    def __init__(self, summoner_name: str, server: str) -> None:
        
        self._requested_data = {}
        
        # Summoner requested attributes
        self._summoner_name = summoner_name
        self._server = server
        
        # Get ApiKey from .env 
        env_loader = EnvLoader()
        try:
            self._api_key = env_loader.get("RIOT_API_KEY")
            
        except EnvironmentError:
            raise RiotApiKeyNotFound()
        
        # Initialize all the needed classes
        self.api_client = ApiClient(server=self.server, api_key=self.api_key, debug=True)
        self.db_manager = DbManager(puuid=self._puuid)
        self.data_formatter = DataFormatter()
        
        # Always request summoner info based on summoner name to Riot API
        self.summoner_info = async_to_sync(self.api_client.get_summoner_by_name)(summoner_name=self.summoner_name)
        self._puuid: str = self.summoner_info["puuid"]
        self._id: str = self.summoner_info["id"]
            
        
    # Properties
    @property
    def requested_data(self):
        return self._requested_data
    
    @requested_data.setter
    def requested_data(self, new_data):
        self._requested_data = new_data
        
    @property
    def api_key(self):
        return self._api_key
    
    @property
    def puuid(self):
        return self._puuid
    
    @property
    def id(self):
        return self._id
    
    @property
    def summoner_name(self):
        return self._summoner_name
    
    @property
    def server(self):
        return self._server
    
    
    def fetch_requested_data(self): #TODO Refactorizar este metodo para que esta funcionalidad se haga en la clase DataFormatter. Esta clase debe enviar una peticion de los datos ya formateados a la base de datos mediante el DataFormatter.
        
        # If the summoner puuid is already in the database
        if self.db_manager.is_puuid_in_database():
            
            # Check how much time has been since last update
            now = int(time.time())
            last_update = self.db_manager.last_update()
            
            if (now - last_update) > self.SECONDS_BEFORE_UPDATING_DATABASE:
                
                # Request data from Riot API using ApiClient
                summoner_request = async_to_sync(self.api_client.get_summoner_by_name)(
                    summoner_name=self.summoner_name
                    )
                ranked_stats_request = async_to_sync(self.api_client.get_league_by_summoner)(
                    summoner_id=self._id
                    )
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