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
        
        RankedStats.objects.update_or_create(queue_type=queue, summoner=self.summoner_instance, defaults=defaults)

    def _update_summoner_match(self, match_id: str, data: dict):
        
        item_purchase = [Item.objects.get(id=item_id) for item_id in data["item_ids"]]
        
        summoner_spells = [SummonerSpell.objects.get(id=spell_id) for spell_id in data["summoner_spells"]]
        
        defaults = {
            "id": match_id,
            "season_id": data["season_id"],
            "queue_id": data["queue_id"],
            "game_mode": data["game_mode"],
            "game_type": data["game_type"],
            "champion_name": data["champion_name"],
            "win": data["win"],
            "kills": data["kills"],
            "deaths": data["deaths"],
            "assists": data["assists"],
            "kda": data["kda"],
            "minion_kills": data["minion_kills"],
            "vision_score": data["vision_score"],
            "team_position": data["team_position"],
            
            "summoner": self.summoner_instance,
            "item_purchase": item_purchase,
            "summoner_spells": summoner_spells,
        }
        
        SummonerMatch.objects.update_or_create(id=match_id, defaults=defaults)