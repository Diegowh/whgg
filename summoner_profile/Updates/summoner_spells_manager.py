import requests

from ..DataManager.db_manager import DbManager


class SummonerSpellsManager:
    
    SUMMONER_SPELLS_URL = "https://ddragon.leagueoflegends.com/cdn/13.22.1/data/en_US/summoner.json"
    
    
    def __init__(self) -> None:
        
        self._summ_spells = []
        
        # Create an instance for DbManager
        self.db_manager = DbManager()
        
    def summ_spells(self) -> list:
        '''
        Returns all summoner spells collected data
        '''
        return self._summ_spells
    
    def _filter(self, json: dict) -> list:
        '''
        Filters the desired data from the given json to return it as a list
        '''
        summ_spells = []
        
        if "data" in json:
            
            data = json["data"]
            
            for spell_id, spell_info in data.items():
                
                spell = {
                    "id": spell_id,
                    "name": spell_info["name"],
                    "description": spell_info["description"],
                    "image_name": spell_info["image"]["full"],
                    "sprite_name": spell_info["image"]["sprite"],
                }
                
                summ_spells.append(spell)
                
            self._summ_spells = summ_spells
            
    def _fetch(self):
        
        response = requests.get(self.SUMMONER_SPELLS_URL)
        summ_spells_json = response.json()
        
        if isinstance(summ_spells_json, dict) and len(summ_spells_json) > 0:
            self._filter(summ_spells_json)

        
    def update(self):
        '''
        Updates self._summ_spells to the latest values collecting the data from DataDragon'''
        try:
            self._fetch()
        
        except Exception as e:
            print(e)
            return None
        
        # Save the new summoner spells data into the database
        self.db_manager.update_summoner_spells(summoner_spells=self.summ_spells())