import asyncio
import time
import datetime



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
        self.previously_pending = 0
        
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
        
    
    async def _reset(self):
        
        # Checks if the time window is over
        while self.time + self.duration >= int(time.mktime(datetime.datetime.utcnow().timetuple())):
            await asyncio.sleep(1)
        
        
        # Reset time and count
        self.time = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        self.count = 0
        
        # Manage the count of pending requests
        self.previously_pending += self.currently_pending
        self.currently_pending = 0
        
        
        # Increase the num for the time window
        self.num += 1
        
        # The window is not synced with the server anymore
        self.synced = False
        
    
    async def get_back(self, num: int, timestamp: int, limit=None):
        async with self.back_lock:
            
            # If the current time window is up to date
            if self.time + self.duration > timestamp:
                
                if self.num == num:
                    self.currently_pending -= 1
                else:
                    self.previously_pending -= 1
                    self.count += 1