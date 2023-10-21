import os

class ApiClient:
    def __init__(self) -> None:
        self.api_key = os.environ['RIOT_API_KEY']