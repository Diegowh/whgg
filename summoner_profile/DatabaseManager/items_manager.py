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
        
        response = requests.get(self.VERSIONS_URL)
        if response.status_code == 200:
            versions_json = response.json()
            
            
        if isinstance(versions_json, list) and len(versions_json) > 0:
            
            self.latest_version = versions_json[0]
            
            
    def update(self):
        
        previous_version = self.latest_version
        
        self.get_latest_version()
        
        if not (previous_version == self.latest_version):
            
            response = requests.get(self.ITEMS_URL)
            if response.status_code == 200:
                items_json = response.json()
                
            
            if isinstance(items_json, dict) and len(items_json) > 0:
                #TODO: Create fetch method 
                pass
        
        # If the version is the same
        else:
            self.is_updated = True