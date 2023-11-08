from ..models.models import (
    ChampionStats,
    Item,
    Participant,
    RankedStats,
    SummonerMatch,
    Summoner,
    Version,
    SummonerSpell,
    
)

class DbManager:
    
    def __init__(self, puuid) -> None:
        
        self.puuid = puuid
        self.summoner_instance = Summoner.objects.get(puuid=self.puuid)
    
    def update(self, puuid: str, data: dict):
        # Here all update methods are called
        pass
    
    def _update_summoner(self, data: dict):
        
        defaults = {
            "id": data["id"],
            "name": data["name"],
            "server": data["server"],
            "icon_id": data["icon_id"],
            "summoner_level": data["summoner_level"],
            "last_update": data["last_update"]
        }
        
        Summoner.objects.update_or_create(puuid=self.puuid, defaults=defaults)


    def _update_ranked_stats(self, queue: str, data: dict):
        
        defaults = {
            "queue_type": queue,
            "rank": data["rank"],
            "league_points": data["league_points"],
            "wins": data["wins"],
            "losses": data["losses"],
            "winrate": int(round(data["winrate"])),
            "summoner": self.summoner_instance
        }
        
        RankedStats.objects.update_or_create(queue_type=queue, summoner=summoner_instance, defaults=defaults)
