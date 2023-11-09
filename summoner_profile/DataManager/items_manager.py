'''
Items manager periodically updates and collect all items data from League of Legends
'''

import requests

from ..models.item import Item

from .db_manager import DbManager


class ItemsManager:
    
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json" # This url provides an updated json file with all versions
    ITEMS_URL = "http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json"
    
    
    def __init__(self) -> None:
        
        self._items = []
        
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
                
                
        except Exception as e:
            print(e)
            return None
            
        if isinstance(items_json, dict) and len(items_json) > 0:
            self._fetch(items_json)
            
            
        
        # Save the new items data into the database
        self.update_database()
        
        
        
    def update_database(self):
        
        for item in self.items():
            
            Item.objects.update_or_create(
                id=item["id"],
                defaults=item
            )
    
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