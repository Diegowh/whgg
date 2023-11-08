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
        
        self.data = {}
    
    def update(self, data: dict):
        
        self.data = data
    
    def _update_summoner(self):
        
        summoner_data = self.data["summoner"]
        
        defaults = {
            "id": summoner_data["id"],
            "name": summoner_data["name"],
            "server": summoner_data["server"],
            "icon_id": summoner_data["icon_id"],
            "summoner_level": summoner_data["summoner_level"],
            "last_update": summoner_data["last_update"]
        }
        
        Summoner.objects.update_or_create(puuid=self.puuid, defaults=defaults)


    def _update_ranked_stats(self):
        
        for queue, ranked_stats in self.data["ranked_stats"].items():
            
            defaults = {
                "queue_type": queue,
                "rank": ranked_stats["rank"],
                "league_points": ranked_stats["league_points"],
                "wins": ranked_stats["wins"],
                "losses": ranked_stats["losses"],
                "winrate": int(round(ranked_stats["winrate"])),
                "summoner": self.summoner_instance
            }
            
            RankedStats.objects.update_or_create(queue_type=queue, summoner=self.summoner_instance, defaults=defaults)

    def _update_summoner_matches(self):
        
        matches_to_update = self.data["last_20_matches"]
        
        for match_data in matches_to_update:
            match_id = match_data["id"]
            
            
            item_purchase = [Item.objects.get(id=item_id) for item_id in match_data["item_ids"]]
            summoner_spells = [SummonerSpell.objects.get(id=spell_id) for spell_id in match_data["summoner_spells"]]
        
            defaults = {
                "id": match_id,
                "season_id": match_data["season_id"],
                "queue_id": match_data["queue_id"],
                "game_mode": match_data["game_mode"],
                "game_type": match_data["game_type"],
                "champion_name": match_data["champion_name"],
                "win": match_data["win"],
                "kills": match_data["kills"],
                "deaths": match_data["deaths"],
                "assists": match_data["assists"],
                "kda": match_data["kda"],
                "minion_kills": match_data["minion_kills"],
                "vision_score": match_data["vision_score"],
                "team_position": match_data["team_position"],
                
                "summoner": self.summoner_instance,
                "item_purchase": item_purchase,
                "summoner_spells": summoner_spells,
            }
        
            SummonerMatch.objects.update_or_create(id=match_id, defaults=defaults)