
from .base_manager import BaseManager


class ItemsManager(BaseManager):
    
    ITEMS_URL = "http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json"
    
    
    def __init__(self) -> None:
        super().__init__(url=self.ITEMS_URL)
        
    def _filter(self, json: dict) -> list:
        '''
        Filters the desired data from the given json to return it as a list
        '''
        items = []
        
        if 'data' in json:
            items_data: dict = json['data']
            
            for item_id, item_info in items_data.items():
                
                item = {
                    'id': item_id,
                    'name': item_info['name'],
                    'plaintext': item_info['plaintext'],
                    'description': item_info['description'],
                    'gold_base': item_info['gold']['base'],
                    'gold_total': item_info['gold']['total'],
                }

                items.append(item)
        
            self._data = items
    