from os import name
from tkinter import image_names
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
    
@dataclass
class ChampionStatsData:
    id: str
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
    summoner: str
    item_purchase: List[int]
    summoner_spells: List[int]
    
@dataclass
class ParticipantData:
    id: int
    puuid: str
    name: str
    champion_name: str
    team_id: int
    summoner_match: str
    match: str
    
@dataclass
class ItemData:
    id: int
    name: str
    plaintext: str
    description: str
    gold_base: int
    gold_total: int
    
@dataclass
class SummonerSpellData:
    id: int
    name: str
    description: str
    image_name: str
    sprite_name: str
    
    
    # TODO: Estudiar en profundidad las dataclasses. Comenzar por este video: https://www.youtube.com/watch?v=vBH6GRJ1REM
    # TODO: El camino a seguir parece ser tratar a los paquetes de datos que van a enviarse por la API Gateway como clases predefinidas como dataclasses, ya que parece que permiten algun tipo de conversion a diccionarios/tuplas. Investigar bien esto para estar seguro de como funciona y en que manera se puede implementar para evitar andar hardcodeando los diccionarios de una clase a otra