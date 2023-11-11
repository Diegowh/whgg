import requests


from .items_manager import ItemsManager
from ..models.version import Version

from ..controllers.db_manager import DbManager


class Updater:
    '''
    Manages the updates on the json files based on the new versions of league of legends.
    '''
    
    
    # Json data urls
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
    
    def __init__(self) -> None:
        
        self.db_manager = DbManager()
        
        self.latest_version = None
        self.previous_version = None
        
        # Checks if there is a previous version on the database
        version_query = Version.objects.first()
        if version_query:
            self.previous_version = version_query.version
            self.latest_version = self.previous_version
        
        
    def check_for_updates(self):
        
        try:
            response = requests.get(self.VERSIONS_URL)
            versions_json = response.json()
            
            
        except Exception as e:
            print(e)
            return None
            
        if isinstance(versions_json, list) and len(versions_json) > 0:
            
            self.latest_version = versions_json[0]
            
            # Saves it on the database
            self._save_latest_version()
            
        else:
            print("An error ocurred trying to validate versions_json type or length")
            return None
        
    def is_updated(self) ->bool:
        '''
        Returns True if the latest version is different to the previous one.
        '''
        return self.latest_version != self.previous_version if self.latest_version and self.previous_version else False
    
        
    def _save_latest_version(self):
        '''
        Saves self.latest_version into the database.
        '''
        Version.objects.update_or_create(
            defaults= {
                'version': self.latest_version,
            }
        )
        
    def update_items(self):
        
        items_manager = ItemsManager()
        
        if items_manager.is_updated():
            
            items = items_manager.data
            
            self.db_manager.update_items(items=items)