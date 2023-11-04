from datetime import datetime
import dotenv
import os

from django.core.cache import cache
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


class RequestedDataManager:
    
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
        
        # Cache the summoner puuid to avoid making multiple requests to the API
        self._puuid = cache.get(f'summoner_puuid_{summoner_name}')
        if self._puuid is None:
            self._puuid = async_to_sync(self.api_client.get_summoner_by_name)(summoner_name)
        
    def summoner_puuid(self):
        
    
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
        