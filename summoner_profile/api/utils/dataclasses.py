from dataclasses import dataclass

@dataclass
class SummonerInfo:
    name: str
    icon_id: int
    account_level: int

@dataclass
class SoloqInfo:
    rank: str
    league_points: int
    wins: int
    losses: int
    winrate: int

@dataclass
class FlexInfo:
    rank: str
    league_points: int
    wins: int
    losses: int
    winrate: int

@dataclass
class RankedInfo:
    soloq: SoloqInfo
    flex: FlexInfo
    
@dataclass
class ChampionStats:
    name: str
    games: int
    winrate: int
    kda: float
    kills: float
    deaths: float
    assists: float