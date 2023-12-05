from typing import List
from dataclasses import dataclass, field

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
    id: str
    name: str
    key: int
    description: str
    image_name: str
    sprite_name: str

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
    champion_played: str = None
    win: bool = None
    kills: int = None
    deaths: int = None
    assists: int = None
    kda: float = None
    minion_kills: int = None
    vision_score: int = None
    team_position: str = None
    team_id: int = None
    item_purchase: List[ItemData] = field(default_factory=list)
    summoner_spells: List[SummonerSpellData] = field(default_factory=list)
    participants: List[ParticipantData] = field(default_factory=list)

    def to_dict(self):
        return {
            'id': self.id,
            'game_start': self.game_start,
            'game_end': self.game_end,
            'game_duration': self.game_duration,
            'game_mode': self.game_mode,
            'game_type': self.game_type,
            'champion_played': self.champion_played,
            'win': self.win,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'kda': self.kda,
            'minion_kills': self.minion_kills,
            'vision_score': self.vision_score,
            'team_position': self.team_position,
            'team_id': self.team_id,
            'item_purchase': [item.to_dict() for item in self.item_purchase],
            'summoner_spells': [spell.to_dict() for spell in self.summoner_spells],
            'participants': [participant.to_dict() for participant in self.participants],
        }
    
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
    match_data_list: List[MatchData]
    
    def to_dict(self):
        return {
            'summoner_data': self.summoner_data.to_dict(),
            'ranked_stats_data_list': [data.to_dict() for data in self.ranked_stats_data_list],
            'champion_stats_data_list': [data.to_dict() for data in self.champion_stats_data_list],
            'match_data_list': [match.to_dict() for match in self.match_data_list],
        }