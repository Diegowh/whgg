'''
Items manager periodically updates and collect all items data from League of Legends
'''

import requests

from .db_manager import DbManager


class ItemsManager:
    
    ITEMS_URL = "http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json"
    
    
    def __init__(self) -> None:
        
        self._items = []
        
        # Create an instance for DbManager
        self.db_manager = DbManager()
        
    def items(self) -> list:
        '''
        Returns all item collected data
        '''
        return self._items
        
            
    def update(self):
        '''
        Updates self._items to the latest values collecting the data from DataDragon
        '''
        # Try to find a latest version
        try:
            response = requests.get(self.ITEMS_URL)
            items_json = response.json()
                
            if isinstance(items_json, dict) and len(items_json) > 0:
                self._fetch(items_json)
                
        except Exception as e:
            print(e)
            return None
            
            
            
        
        # Save the new items data into the database
        self.db_manager.update_items(items=self.items())
        
    
    def _fetch(self, json: dict) -> list:
        '''
        Collects the desired data from the given json to return it as a list
        '''
        items = []
        
        if 'data' in json:
            items = json['data']
            
            for item_id, item_info in items.items():
                
                item = {
                    'id': item_id,
                    'name': item_info['name'],
                    'plaintext': item_info['plaintext'],
                    'description': item_info['description'],
                    'gold_base': item_info['gold']['base'],
                    'gold_total': item_info['gold']['total'],
                }

                items.append(item)
        
            self._items = items