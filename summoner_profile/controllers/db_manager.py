from summoner_profile.models import (
    ChampionStats,
    Item,
    Participant,
    RankedStats,
    Match,
    Summoner,
    SummonerSpell,
    
)
from summoner_profile.utils.utils import calculate_kda
from .data_manager import DataManager

from summoner_profile.utils.dataclasses import (
    ParticipantData,
    RankedStatsData,
    RequestData,
    SummonerData,
    MatchData,
    ResponseData
)


class DbManager:
    
    def __init__(self) -> None:
        
        
        self.puuid = self.data_manager.get_summoner_puuid()
        self.data = {}
        
        self._summoner_instance = None
            
            
    @property
    def summoner_instance(self):
        return self._summoner_instance
    
    @summoner_instance.setter
    def summoner_instance(self, new_value: Summoner):
        if isinstance(new_value, Summoner):
            self._summoner_instance = new_value
        
    
    def is_puuid_in_database(self) -> bool:
        
        return Summoner.objects.filter(puuid=self.puuid).exists()
    
    def last_update(self) -> int:
        
        return Summoner.objects.get(puuid=self.puuid).last_update
    
    def update(self, data: dict):
        
        if self.puuid:
            
            # Set given data to self.data
            self.data = data
            
            # Update the database
            self._update_summoner()
            self._update_ranked_stats()
            self._update_summoner_matches()
            self._update_champion_stats()
        
        else:
            raise Exception("Summoner PuuID was not given. Are you sure you want to use this method?")
            
    
    def update_summoner(self, data: SummonerData):
        
        defaults = {
            "id": data.id,
            "name": data.name,
            "icon_id": data.icon_id,
            "summoner_level": data.summoner_level,
            "last_update": data.last_update,
        }
        
        Summoner.objects.update_or_create(puuid=data.puuid, defaults=defaults)
        
        # Obtengo la instancia del summoner que acabo de actualizar para poder usarla en los siguientes metodos
        self.summoner_instance = Summoner.objects.get(puuid=self.puuid)


    def update_ranked_stats(self, data: list[RankedStatsData]):
        
        for ranked_stats in data:
            defaults: {
                "tier": ranked_stats.tier,
                "rank": ranked_stats.rank,
                "league_points": ranked_stats.league_points,
                "wins": ranked_stats.wins,
                "losses": ranked_stats.losses,
                "winrate": ranked_stats.winrate,
                
            }
            
            RankedStats.objects.update_or_create(queue_type=ranked_stats.queue_type, summoner=self.summoner_instance, defaults=defaults)

    def update_match_data(self, data: list[MatchData]):
        
        for match_data in data:
        
            defaults = {
                "game_start": match_data.game_start,
                "game_end": match_data.game_end,
                "game_duration": match_data.game_duration,
                "game_mode": match_data.game_mode,
                "game_type": match_data.game_type,
                "champion_played": match_data.champion_played,
                "win": match_data.win,
                "kills": match_data.kills,
                "deaths": match_data.deaths,
                "assists": match_data.assists,
                "kda": match_data.kda,
                "minion_kills": match_data.minion_kills,
                "vision_score": match_data.vision_score,
                "team_position": match_data.team_position,
                "team_id": match_data.team_id,
                
                "summoner": self.summoner_instance,
            }
        
            match, created = Match.objects.update_or_create(id=match_data.id, defaults=defaults)
            
            # Obtiene los objetos Item para los items comprados en este match
            items = Item.objects.filter(id__in=match_data.item_purchase)
            
            # Agrega los items al match
            match.item_purchase.set(items)
            
            # Obtiene los objetos Participant para los participantes de este match
            summoner_spells = SummonerSpell.objects.filter(id__in=match_data.summoner_spells)
            
            #  Agrego los summoner spells al match
            match.summoner_spells.set(summoner_spells)
            
            
    def update_participants_data(self, data: list[ParticipantData]):
        
        for participant_data in data:
            
            # Obtengo la instancia de Match a la que pertenece el participante
            match_instance = Match.objects.get(id=participant_data.match)
            
            defaults = {
                "name": participant_data.name,
                "champion_name": participant_data.champion_name,
                "team_id": participant_data.team_id,
            }
            
            Participant.objects.update_or_create(puuid=participant_data.puuid, match=match_instance, defaults=defaults)
            
            
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
            
    def update_champion_stats(self):
            
            # Obtiene los matches del summoner
            matches = Match.objects.filter(summoner=self.summoner_instance)
            
            for match_ in matches:
                
                # Obtiene el nombre del campeon jugado en ese match
                champion_name = match_.champion_played
                
                # Busca una entrada existente de ChampionStats con ese nombre de campeon y summoner
                champion_stats, created = ChampionStats.objects.get_or_create(
                    name=champion_name,
                    summoner=self.summoner_instance,
                    defaults = {
                        "games": 1,
                        "wins": 1 if match_.win else 0,
                        "losses": 1 if not match_.win else 0,
                        "winrate": 100 if match_.win else 0,
                        "kills": match_.kills,
                        "deaths": match_.deaths,
                        "assists": match_.assists,
                        "kda": calculate_kda(match_.kills, match_.deaths, match_.assists),
                        "minion_kills": match_.minion_kills,
                    }
                )
                
                # Si existe, actualiza sus estadisticas
                if not created:
                    
                    self._update_stats(champion_stats, match_)
                    
    def _update_stats(self, champion_stats: ChampionStats, match: Match):
        
        # Actualiza las estadisticas del campeon
        champion_stats.games += 1
        champion_stats.wins += 1 if match.win else 0
        champion_stats.losses += 1 if not match.win else 0
        champion_stats.winrate = int((champion_stats.wins / champion_stats.games) * 100)
        champion_stats.kills += match.kills
        champion_stats.deaths += match.deaths
        champion_stats.assists += match.assists
        champion_stats.kda = calculate_kda(champion_stats.kills, champion_stats.deaths, champion_stats.assists)
        champion_stats.minion_kills += match.minion_kills
        
        champion_stats.save()
            
    # Periodic Updates
    def update_items(self, items: list):
        
        for item in items:
            
            Item.objects.update_or_create(
                id=item["id"],
                defaults=item,
                
            )
            
    def update_summoner_spells(self, summoner_spells: list):
        
        for spell in summoner_spells:
            
            SummonerSpell.objects.update_or_create(
                id=spell["id"],
                defaults=spell,
            )
            
    def get_summoner_data_from_db(self, puuid: str) -> SummonerData:
        
        summoner = Summoner.objects.get(puuid=puuid)
        
        return SummonerData(
            puuid=summoner.puuid,
            id=summoner.id,
            name=summoner.name,
            icon_id=summoner.icon_id,
            summoner_level=summoner.summoner_level,
            last_update=summoner.last_update,
        )
        
    def get_ranked_stats_data_list_from_db(self) -> list[RankedStatsData]:
            
            ranked_stats = RankedStats.objects.filter(summoner=self.summoner_instance)
            
            ranked_stats_data_list: list[RankedStatsData] = []
            
            for ranked_stats_entry in ranked_stats:
                
                ranked_stats_data_list.append(
                    RankedStatsData(
                        queue_type=ranked_stats_entry.queue_type,
                        tier=ranked_stats_entry.tier,
                        rank=ranked_stats_entry.rank,
                        league_points=ranked_stats_entry.league_points,
                        wins=ranked_stats_entry.wins,
                        losses=ranked_stats_entry.losses,
                        winrate=ranked_stats_entry.winrate,
                    )
                )
                
            return ranked_stats_data_list
    
    def get_response_data(self) -> ResponseData:
        ResponseData (
            summoner_data=self.get_summoner_data_from_db(),
            ranked_stats_data_list=self.get_ranked_stats_data_list_from_db(),
        )
        
        
    # Metodos para pedir a DataManager que obtenga los datos de la API de Riot
    
    def fetch_summoner_data_from_api(self) -> SummonerData:
        
        return self.data_manager.get_summoner_data(summoner_name=self.request.summoner_name
                    )
    def fetch_ranked_stats_data_from_api(self) -> list:
        
        return self.data_manager.get_ranked_stats_data()