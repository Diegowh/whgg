from mimetypes import init
from .db_manager import DbManager


class DataFormatter:
    
    def __init__(self) -> None:
        pass
    
    
    def filter(self, data: dict, type: str):
        
        match type:
            case "summoner":
                self.filter_summoner(data=data)
            case "ranked":
                self.filter_ranked(data=data)
            case "match":
                self.filter_match(data=data)
                