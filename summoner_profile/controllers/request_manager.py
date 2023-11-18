from datetime import datetime
import re
import dotenv
import os
import time
import asyncio

from asgiref.sync import async_to_sync

from summoner_profile.models import summoner

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
from summoner_profile.utils.env_loader import EnvLoader
from summoner_profile.utils.utils import (
    hours_to_seconds,
    calculate_kda,
)


class RequestManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    def __init__(self, summoner_name: str, server: str) -> None:
        
        self._profile_data = {}
        
        # Summoner requested attributes
        self._summoner_name = summoner_name
        self._server = server
        
        # Get ApiKey from .env 
        env_loader = EnvLoader()
        try:
            self._api_key = env_loader.get("RIOT_API_KEY")
            
        except EnvironmentError:
            raise RiotApiKeyNotFound()
        
        # Initialize classes
        self.api_client = ApiClient(server=self.server, api_key=self.api_key, debug=True)
        self.db_manager = DbManager(puuid=self._puuid)
        self.data_formatter = DataFormatter()
        
        # Always request summoner info from API because the summoner name can change for the same puuid
        self.summoner_info = async_to_sync(self.api_client.get_summoner_by_name)(summoner_name=self.summoner_name)
        self._puuid: str = self.summoner_info["puuid"]
        self._id: str = self.summoner_info["id"]
            
        
    # Properties
    @property
    def profile_data(self):
        return self._profile_data
    
    @profile_data.setter
    def profile_data(self, new_data):
        self._profile_data = new_data
        
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
    
    
    # Creo este metodo porque posiblemente refactorice los otros metodos y no se incluiran en RequestManager
    def get(self):
        self._fetch_requested_data()
        return self.profile_data
        
        
    def _fetch_requested_data(self): 
        
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
                last_matches_request = ...
                
                # Send the data to DbManager to update the database
                pass
            
            else:
                # Return summoners data from the database without an update
                pass
        
        # If the summoner puuid is not in the database
        else:
            # Update the database
            pass
    
    # Match data
    
    # Consigue los match ids de la ultima temporada
    def all_match_ids(self) -> list:
        MAX_MATCHES = 5000 # To set a limit to the number of matches to request
        REQUEST_CAP = 100 # The api only allows to request 100 matches at a time
        season_start = int(datetime(2023, 1, 14).timestamp()) # TODO Get this date from the database
        
        match_ids = []
        params = {
            "startTime": season_start,
            "type": "ranked",
        }
        
        for start_index in range(0, MAX_MATCHES, REQUEST_CAP):
            
            params["start"] = start_index
            params["count"] = int(min(REQUEST_CAP, MAX_MATCHES - start_index))# To avoid requesting more matches than the limit

            
            matchlist_response: list = async_to_sync(self.api_client.get_matchlist_by_puuid)(
                puuid=self.puuid,
                params= params,
                )
            
            if matchlist_response == []:
                break
            
            match_ids += matchlist_response
        
        return match_ids
    
    # Obtiene los datos de un match dado su id
    def matches_data(self, match_ids):
        
        return [async_to_sync(self.api_client.get_match)(match_id=match_id) for match_id in match_ids]
        
        
    # Formatea los datos de los matches para ser guardados en la base de datos
    def process_response(self, response):
        
        summoner_match_data = {
            
            "id": response["metadata"]["matchId"],
            "game_start": response["info"]["gameStartTimestamp"],
            "game_end": response["info"]["gameEndTimestamp"],
            "game_duration": response["info"]["gameDuration"],
            "game_mode": response["info"]["gameMode"],
            "game_type": response["info"]["gameType"],
        }
        
        participants_info = response["info"]["participants"]
        
        for participant in participants_info:
            
            if participant["puuid"] == self.puuid:
                    
                summoner_match_data["champion_played"] = participant["championName"]
                summoner_match_data["win"] = participant["win"]
                summoner_match_data["kills"] = participant["kills"]
                summoner_match_data["deaths"] = participant["deaths"]
                summoner_match_data["assists"] = participant["assists"]
                
                summoner_match_data["kda"] =  calculate_kda(
                    kills=participant["kills"],
                    deaths=participant["deaths"],
                    assists=participant["assists"],
                )
                
                summoner_match_data["minion_kills"] = sum(
                    participant["totalMinionsKilled"],
                    participant["neutralMinionsKilledTeamJungle"],
                    participant["neutralMinionsKilledEnemyJungle"],
                )
                