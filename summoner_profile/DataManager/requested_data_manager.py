from datetime import datetime
import dotenv
import os
import time

from asgiref.sync import async_to_sync

from .dataclasses import (
    
    SummonerInfo,
    SoloqInfo,
    FlexInfo,
    RankedInfo,
    ChampionStats,
    
)

from ..api.api_client import ApiClient
from ..api.utils.exceptions import RiotApiKeyNotFound
from ..models.summoner import Summoner
from ..utils.utils import hours_to_seconds


class RequestedDataManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    def __init__(self, summoner_name: str, server: str) -> None:
        
        # Set default structure for self.data
        self.data = {
            
            "summoner_info": {
                "name": None,
                "icon_id": None,
                "account_level": None,
            },
            
            "ranked_info": {
                
                "soloq": {
                    "rank": None,
                    "league_points": None,
                    "wins": None,
                    "losses": None,
                    "winrate": None,
                    },
                    
                "flex": {
                    "rank": None,
                    "league_points": None,
                    "wins": None,
                    "losses": None,
                    "winrate": None,
                    },
            },
            
            "champion_stats": [],
            
            "last_20_matches":[],
        }
        
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
        
        
        self.api_client = ApiClient(server=self.server, api_key=api_key, debug=True)
        
        
        # To avoid repetitive requests for the IDs
        self.summoner_info = async_to_sync(self.fetch_summoner)()
        self._puuid: str = self.summoner_info["puuid"]
        self._id: str = self.summoner_info["id"]
        
    
    def _add_summoner_info(self, summoner_info: SummonerInfo):
        """Add SummonerInfo data into self.data."""
        
        self.data["summoner_info"]["name"] = summoner_info.name
        self.data["summoner_info"]["icon_id"] = summoner_info.icon_id
        self.data["summoner_info"]["account_level"] = summoner_info.account_level
    
    def _add_ranked_info(self, ranked_info: RankedInfo):
        """Add RankedInfo data into self.data."""
        
        self.data["ranked_info"]["soloq"]["rank"] = ranked_info.soloq.rank
        self.data["ranked_info"]["soloq"]["league_points"] = ranked_info.soloq.league_points
        self.data["ranked_info"]["soloq"]["wins"] = ranked_info.soloq.wins
        self.data["ranked_info"]["soloq"]["losses"] = ranked_info.soloq.losses
        self.data["ranked_info"]["soloq"]["winrate"] = ranked_info.soloq.winrate

        self.data["ranked_info"]["flex"]["rank"] = ranked_info.flex.rank
        self.data["ranked_info"]["flex"]["league_points"] = ranked_info.flex.league_points
        self.data["ranked_info"]["flex"]["wins"] = ranked_info.flex.wins
        self.data["ranked_info"]["flex"]["losses"] = ranked_info.flex.losses
        self.data["ranked_info"]["flex"]["winrate"] = ranked_info.flex.winrate
    
    def _add_champion_stats(self, champion_stats: ChampionStats):
        
        all_champion_stats = []
        
        all_champion_stats.append(champion_stats)
        
        
    def is_puuid_in_database(self) -> bool:
        '''
        Checks if the current instance's PUUID exists in the database.
        
        Returns:
            bool: True if PUUID exists in the database, False otherwise.
        '''
        return Summoner.objects.filter(puuid=self.puuid).exists()
    
    
    def get_last_update(self):
        '''
        Returns last_update for self.puuid from Summoner model
        '''
        return Summoner.objects.get(puuid=self.puuid).last_update
    
    def get_data_from_database(self):
        
        # If the summoner puuid is already in the database
        if self.is_puuid_in_database():
            
            # Check how much time has been since last update
            now = int(time.time())
            last_update = self.get_last_update()
            
            if (now - last_update) > self.SECONDS_BEFORE_UPDATING_DATABASE:
                # Update the database
                pass
            
            else:
                # Return summoners data from the database without an update
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
    
    async def fetch_ranked_stats(self):
        '''
        Returns structured data ready to send it to RankedStats model
        '''
        response = await self.api_client.get_league_by_summoner()
        