import os
import dotenv

class EnvLoader:
    def __init__(self) -> None:
        
        try:
            dotenv.load_dotenv()
        
        except EnvironmentError:
            print("Could not load .env file")
            
    
    def get(self, key: str) -> str:
        
        value = os.getenv(key)
        if value is None:
            raise EnvironmentError(f"Could not find environment variable {key}")
        
        return value