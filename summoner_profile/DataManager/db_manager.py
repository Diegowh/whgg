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


from django.db.models import Model


class DbManager:
    
    def __init__(self, puuid = None) -> None:
        
        self.puuid = puuid
        self.data = {}
        
        if puuid:
            self.summoner_instance = Summoner.objects.get(puuid=self.puuid)
    
    def update(self, data: dict = None, model: Model = None):
        
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
                "winrate": int(round(ranked_stats["winrate", 0])),
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
            
            
            # Obtain match participants
            participants: list = match_data["participants"]
            
            self._update_participants(participants)
            
            
            
    def _update_participants(self, match_participants):
        
        for participant_data in match_participants:
            
            participant_id = participant_data["id"]
            
            defaults = {
                "puuid": participant_data["puuid"],
                "name": participant_data["name"],
                "champion_name": participant_data["champion_name"],
                "team_id": participant_data["team_id"],
            }
            
            # Each participant represents a player in a summoner match and is unique and unchangeable for that specific match. 
            # Even if the data (puuid, name, champion_name, and team_id) for two different participants is the same, 
            # they will always refer to distinct instances in a summoner match.
            Participant.objects.get_or_create(id=participant_id, defaults=defaults)
            
            
    def _update_champion_stats(self):
        
        all_champion_stats = self.data["champion_stats"]
        
        for champion_stats_entry in all_champion_stats:
            
            champion_stats_id = champion_stats_entry["id"]
            
            defaults = {
                "id": champion_stats_id,
                "name": champion_stats_entry["name"],
                "games": champion_stats_entry["games"],
                "wins": champion_stats_entry["wins"],
                "losses": champion_stats_entry["losses"],
                "winrate": champion_stats_entry["winrate"],
                "kills": champion_stats_entry["kills"],
                "deaths": champion_stats_entry["deaths"],
                "assists": champion_stats_entry["assists"],
                "kda": champion_stats_entry["kda"],
                "minion_kills": champion_stats_entry["minion_kills"],
                "summoner": self.summoner_instance
            }
            
            ChampionStats.objects.update_or_create(id=champion_stats_id, defaults=defaults)
            
    # Items 
    def update_items(self, items: list):
        
        for item in items:
            
            Item.objects.update_or_create(
                id=item["id"],
                defaults=item,
                
            )