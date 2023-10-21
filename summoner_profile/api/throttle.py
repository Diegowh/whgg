import time

class Throttle():
    def __init__(self) -> None:
        self.BURST_LIMIT = 20
        self.BURST_TIME = 1
        self.SUSTAINED_LIMIT = 100
        self.SUSTAINED_TIME = 120
        
        self.last_request = 0