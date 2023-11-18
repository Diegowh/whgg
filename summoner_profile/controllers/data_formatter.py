from mimetypes import init
import re
from .db_manager import DbManager


class DataFormatter:
    
    def __init__(self) -> None:
        pass
    
    
    def filter(self, data: dict, type: str):
        
        match type:
            case "summoner":
                self.filter_summoner(data=data)
            case "ranked":
                self.filter_ranked(data=data)
            case "match":
                self.filter_match(match_data=data)
                
                
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