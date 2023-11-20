from mimetypes import init
import re

from .api_client import ApiClient
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
    
    def __init__(self, summoner_name: str, api_client: ApiClient) -> None:
        self.summoner_name = summoner_name
        self.api_client = api_client
        
        self._summoner_data: SummonerData = self._create_summoner_data(summoner_name=self.summoner_name)
        
        self.puuid = self._summoner_data.puuid
        self.id = self._summoner_data.id
    
    def get_summoner_data(self) -> SummonerData:
        return self._summoner_data
    
    def get_summoner_puuid(self) -> str:
        return self._summoner_data.puuid
    
    def get_summoner_id(self) -> str:
        return self._summoner_data.id
    
    # Se encarga de obtener los datos de la Api de Riot y crea un objeto SummonerData
    def _create_summoner_data(self) -> SummonerData:
        response = async_to_sync(self.api_client.get_summoner_by_name)(
                    summoner_name=self.summoner_name
                    )
        
        summoner_data = SummonerData(
            puuid=response["puuid"],
            id=response["id"],
            name=response["name"],
            icon_id=response["profileIconId"],
            summoner_level=response["summonerLevel"],
            last_update=response["revisionDate"]
        )
        return summoner_data
                
                
    def _create_ranked_stats_list(self) -> list[RankedStatsData]:
        response: list = async_to_sync(self.api_client.get_league_by_summoner)(
                summoner_id=self.id
                )
        
        ranked_stats_list = []
        
        for queue in response:
            
            ranked_stats_data = RankedStatsData(
                queue_type=queue["queueType"],
                tier=queue["tier"],
                rank=queue["rank"],
                league_points=queue["leaguePoints"],
                wins=queue["wins"],
                losses=queue["losses"],
                winrate=queue["wins"] / (queue["wins"] + queue["losses"]), # TODO: Crea una función para calcular el winrate
                summoner=self.puuid
            )
            ranked_stats_list.append(ranked_stats_data)
        
        return ranked_stats_list
        
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