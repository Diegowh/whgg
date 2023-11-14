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
    
    # TODO: Estudiar en profundidad las dataclasses. Comenzar por este video: https://www.youtube.com/watch?v=vBH6GRJ1REM
    # TODO: El camino a seguir parece ser tratar a los paquetes de datos que van a enviarse por la API Gateway como clases predefinidas como dataclasses, ya que parece que permiten algun tipo de conversion a diccionarios/tuplas. Investigar bien esto para estar seguro de como funciona y en que manera se puede implementar para evitar andar hardcodeando los diccionarios de una clase a otra