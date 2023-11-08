from ..models.models import (
    ChampionStats,
    Item,
    Participant,
    RankedStats,
    SummonerMatch,
    Summoner,
    Version
)

class DbManager:
    
    def __init__(self) -> None:
        pass
    
    def update(self, puuid: str, data: dict):
        # Here all update methods are called
        pass
    
    def _update_summoner(self, puuid:str, data: dict):
        
        defaults = {
            "id": data["id"],
            "name": data["name"],
            "server": data["server"],
            "icon_id": data["icon_id"],
            "summoner_level": data["summoner_level"],
            "last_update": data["last_update"]
        }
        
        Summoner.objects.update_or_create(puuid=puuid, defaults=defaults)