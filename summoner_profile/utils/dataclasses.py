from typing import List
from dataclasses import dataclass

@dataclass
class SummonerData:
    puuid: str
    id: str
    name: str
    icon_id: int
    summoner_level: int
    last_update: int
    
    def to_dict(self):
        return self.__dict__

@dataclass
class RankedStatsData:
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    winrate: int
    summoner: str
    
    def to_dict(self):
        return self.__dict__
    
@dataclass
class ChampionStatsData:
    name: str
    games: int
    wins: int
    losses: int
    winrate: int
    kills: float
    deaths: float
    assists: float
    kda: float
    minion_kills: int
    
    def to_dict(self):
        return self.__dict__
    
@dataclass
class MatchData:
    id: str
    game_start: int
    game_end: int
    game_duration: int
    game_mode: str
    game_type: str
    champion_played: str
    win: bool
    kills: int
    deaths: int
    assists: int
    kda: float
    minion_kills: int
    vision_score: int
    team_position: str
    team_id: int
    summoner: str
    item_purchase: List[int]
    summoner_spells: List[int]

    def to_dict(self):
        return self.__dict__
    
@dataclass
class ParticipantData:
    puuid: str
    name: str
    champion_name: str
    team_id: int
    match: str

    def to_dict(self):
        return self.__dict__
    
@dataclass
class ItemData:
    id: int
    name: str
    plaintext: str
    description: str
    gold_base: int
    gold_total: int

    def to_dict(self):
        return self.__dict__
    
@dataclass
class SummonerSpellData:
    id: int
    name: str
    description: str
    image_name: str
    sprite_name: str

    def to_dict(self):
        return self.__dict__
    
    
@dataclass
class RequestData:
    summoner_name: str
    server: str

    def to_dict(self):
        return self.__dict__

@dataclass
class ResponseData:
    summoner_data: SummonerData
    ranked_stats_data_list: List[RankedStatsData]
    champion_stats_data_list: List[ChampionStatsData]
    match_data_list: List[tuple[MatchData, list[ParticipantData]]]
    
    def to_dict(self):
        return {
            'summoner_data': self.summoner_data.to_dict(),
            'ranked_stats_data_list': [data.to_dict() for data in self.ranked_stats_data_list],
            'champion_stats_data_list': [data.to_dict() for data in self.champion_stats_data_list],
            'recent_match_data_list': [(match.to_dict(), [participant.to_dict() for participant in participants]) for match, participants in self.match_data_list],
        }