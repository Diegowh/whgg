from datetime import datetime

from .dataclasses import (
    
    SummonerInfo,
    SoloqInfo,
    FlexInfo,
    RankedInfo,
    ChampionStats,
    
)

from ..api.api_client import ApiClient

class RequestedDataManager:
    
    def __init__(self, summoner_name: str, region: str) -> None:
        
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
            
            "champion_stats": [
                {
                    "name": None,
                    "games": None,
                    "winrate": None,
                    "kda": None,
                    "kills": None,
                    "deaths": None,
                    "assists": None,
                    
                },
            ]
        }
    
    def _add_summoner_info(self, summoner_info: SummonerInfo):
        # Add SummonerInfo data into self.data.
        pass
    
    def _add_ranked_info(self, ranked_info: RankedInfo):
        # Add RankedInfo data into self.data
        pass
    
    def _add_champion_stats(self, champion_stats: ChampionStats):
        
        all_champion_stats = []
        
        all_champion_stats.append(champion_stats)