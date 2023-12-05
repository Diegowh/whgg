
from .base_manager import BaseManager


class SummonerSpellsManager(BaseManager):
    
    SUMMONER_SPELLS_URL = "https://ddragon.leagueoflegends.com/cdn/13.22.1/data/en_US/summoner.json"
    
    
    def __init__(self) -> None:
        super().__init__(url=self.SUMMONER_SPELLS_URL)
    
    def _filter(self, json: dict):
        '''
        Filters the desired data from the given json to return it as a list
        '''
        summ_spells = []
        data = json["data"]
        
        for spell_id, spell_info in data.items():
            
            spell = {
                "id": spell_id,
                "name": spell_info["name"],
                "key": spell_info["key"],
                "description": spell_info["description"],
                "image_name": spell_info["image"]["full"],
                "sprite_name": spell_info["image"]["sprite"],
            }
            
            summ_spells.append(spell)
            
        self._data = summ_spells
        print(self._data[0])
