import asyncio
import time

class RateLimiter:
    
    def __init__(self, debug, limits: (int, int)=(10, 10), name: str = "") -> None:
        
        # Initialize Async lock for the rate limiter
        self.lock = asyncio.Lock()
        self.back_lock = asyncio.Lock()
        
        # Limits params
        self.limit = limits[0]
        self.duration = limits[1]
        
        # Count and begin of the time window
        self.count = 0
        self.time = 0
        
        # Name of the limiter for debug purposes
        self.name = name
        
        # "ID" of the time window
        self.num = 0
        
        # Init outgoing requests counters
        self.currently_pending = 0
        self.previous_pending = 0
        
        # Synchronicity state with server time window
        self.synced = False
        
        # Debug mode
        self.debug = debug
    
    
    def locked(self):
        return self.lock.locked()
    
    
    def get_duration(self):
        return self.duration
    
    
    def get_limit(self):
        return self.limit
    
    
    def update_limit(self, limit: int):
        self.limit = limit