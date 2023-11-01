'''
Items manager periodically updates and collect all items data from League of Legends
'''

import requests


class ItemsManager:
    
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json" # This url provides an updated json file with all versions
    ITEMS_URL = "http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json"
    
    
    def __init__(self) -> None:
        
        self.latest_version = None
        self.is_updated = False
        
        
    def get_latest_version(self):
        
        try:
            response = requests.get(self.VERSIONS_URL)
            versions_json = response.json()
            
            
        except Exception as e:
            print(e)
            return None
            
        if isinstance(versions_json, list) and len(versions_json) > 0:
            
            self.latest_version = versions_json[0]

            
    def update(self):
        
        previous_version = self.latest_version
        
        self.get_latest_version()
        
        if not (previous_version == self.latest_version):
            
            try:
                response = requests.get(self.ITEMS_URL)
                items_json = response.json()
                
                
            except Exception as e:
                print(e)
                return None
            
            if isinstance(items_json, dict) and len(items_json) > 0:
                self.fetch(items_json)
        
        # If the version is the same
        else:
            self.is_updated = True
            
    
    def fetch(self, json: dict) -> list:
        '''
        Collects the desired data from the given json to return it as a list
        '''
        item_data = []
        
        if 'data' in json:
            items = json['data']
            
            for item_id, item_info in items.items():
                
                item = {
                    'id': item_id,
                    'name': item_info['name'],
                    'plaintext': item_info['plaintext'],
                    'descriptioin': item_info['description'],
                    'gold_base': item_info['gold']['base'],
                    'gold_total': item_info['gold']['total'],
                }

                item_data.append(item)