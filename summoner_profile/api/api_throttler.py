import time

class ApiThrottler():
    def __init__(self) -> None:
        self.BURST_LIMIT = 20 # requests
        self.BURST_TIME = 1 # seconds
        self.SUSTAINED_LIMIT = 100 # requests
        self.SUSTAINED_TIME = 120 # seconds
        
        self.last_request = time.time()
    
    def throttle(self) -> None:
        time_since_last_request = time.time() - self.last_request
        if time_since_last_request < self.BURST_TIME:
            time.sleep((self.BURST_TIME - time_since_last_request) + 0.1)
        self.last_request = time.time()