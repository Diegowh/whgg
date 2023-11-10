import requests

from .db_manager import DbManager


class SummonerSpellsManager:
    
    SUMMONER_SPELLS_URL = "https://ddragon.leagueoflegends.com/cdn/13.22.1/data/en_US/summoner.json"