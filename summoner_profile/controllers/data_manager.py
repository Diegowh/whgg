from mimetypes import init
import re

from .api_client import ApiClient
from .db_manager import DbManager
from summoner_profile.utils.utils import (
    calculate_kda,
)
from asgiref.sync import async_to_sync
from summoner_profile.utils.dataclasses import (
    SummonerData,
    RankedStatsData,
    ChampionStatsData,
    SummonerMatchData,
    ParticipantData,
)

class DataManager:
    
    def __init__(self, db_manager: DbManager, api_client: ApiClient) -> None:
        self.db_manager = db_manager
        self.api_client = api_client
    
    def filter_summoner(self, summoner_name, server) -> SummonerData:
        response = async_to_sync(self.api_client.get_summoner_by_name)(
                    summoner_name=summoner_name
                    )
        
        summoner_data = SummonerData(
            puuid=response["puuid"],
            id=response["id"],
            name=response["name"],
            server=,
            icon_id=response["profileIconId"],
            summoner_level=response["summonerLevel"],
            last_update=response["revisionDate"]
        )
                
    def filter_match(self, match_data) -> dict:
        
        formatted_match_data = {
            
            "id": match_data["metadata"]["matchId"],
            "game_start": match_data["info"]["gameStartTimestamp"],
            "game_end": match_data["info"]["gameEndTimestamp"],
            "game_duration": match_data["info"]["gameDuration"],
            "game_mode": match_data["info"]["gameMode"],
            "game_type": match_data["info"]["gameType"],
        }
        
        participants_info = match_data["info"]["participants"]
        
        for participant in participants_info:
            
            if participant["puuid"] == self.puuid:
                    
                formatted_match_data["champion_played"] = participant["championName"]
                formatted_match_data["win"] = participant["win"]
                formatted_match_data["kills"] = participant["kills"]
                formatted_match_data["deaths"] = participant["deaths"]
                formatted_match_data["assists"] = participant["assists"]
                
                formatted_match_data["kda"] =  calculate_kda(
                    kills=participant["kills"],
                    deaths=participant["deaths"],
                    assists=participant["assists"],
                )
                
                formatted_match_data["minion_kills"] = sum(
                    participant["totalMinionsKilled"],
                    participant["neutralMinionsKilledTeamJungle"],
                    participant["neutralMinionsKilledEnemyJungle"],
                )
                
        return formatted_match_data