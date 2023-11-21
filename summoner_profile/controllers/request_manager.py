from datetime import datetime
import re
import dotenv
import os
import time
import asyncio

from asgiref.sync import async_to_sync

from summoner_profile.models import summoner

from .db_manager import DbManager

from .data_manager import DataManager

from summoner_profile.utils.dataclasses import (
    SummonerData,
    RankedStatsData,
    ChampionStatsData,
    MatchData,
    ParticipantData,
    RequestData,
    
)

from .api_client import ApiClient
from summoner_profile.utils.utils import (
    hours_to_seconds,
    calculate_kda,
)


class RequestManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    def __init__(self, summoner_name: str, server: str) -> None:
        
        self._profile_data = {}
        
        self._request_data: RequestData = RequestData(summoner_name=summoner_name, server=server)
        
        # Summoner requested attributes
        self._summoner_name = summoner_name
        self._server = server
        
        # Initialize classes
        self.api_client = ApiClient(server=self.server, debug=True)
        self.data_manager = DataManager(summoner_name = self.summoner_name, api_client=self.api_client)
        
        # Always request summoner info from API because the summoner name can change for the same puuid
        self._puuid: str = self.data_manager.get_summoner_puuid()
        self._id: str = self.data_manager.get_summoner_id()
        
        
        self.db_manager = DbManager(puuid=self._puuid)
        
        
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
    
    def is_time_to_update(self) -> bool:
        now = int(time.time())
        last_update = self.db_manager.last_update()
        
        return (now - last_update) > self.SECONDS_BEFORE_UPDATING_DATABASE
        
    # TODO La logica de este metodo la tiene que gestionar DbManager
    def _fetch_requested_data(self): 
        
        # If the summoner puuid is already in the database
        if self.db_manager.is_puuid_in_database():
            
            # Check how much time has been since last update
            
            if self.is_time_to_update():
                
                # Request data from Riot API using ApiClient
                summoner_data = self.data_manager.get_summoner_data(summoner_name=self.summoner_name
                    )
                ranked_stats_data = self.data_manager.get_ranked_stats_data()
                recent_matches_data = self.data_manager.get_recent_matches_data()
                
                # Send the data to DbManager to update the database
                pass
            
            else:
                # Return summoners data from the database without an update
                pass
        
        # If the summoner puuid is not in the database
        else:
            # Update the database
            pass
    
