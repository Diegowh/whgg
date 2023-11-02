import requests


class UpdateTracker:
    
    # Json data urls
    SEASONS_URL = "https://static.developer.riotgames.com/docs/lol/seasons.json"
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
    
    def __init__(self) -> None:
        
        self.latest_version = None
        self.previous_version = None
        
    def check_for_updates(self):
        
        try:
            response = requests.get(self.VERSIONS_URL)
            versions_json = response.json()
            
            
        except Exception as e:
            print(e)
            return None
            
        if isinstance(versions_json, list) and len(versions_json) > 0:
            
            self.previous_version = self.latest_version
            
            self.latest_version = versions_json[0]

        else:
            print("An error ocurred trying to validate versions_json type or length")
            return None
        
    def is_updated(self):
        
        if self.latest_version and self.previous_version:
            
            return self.latest_version != self.previous_version
        
        else:
            return False