import asyncio
import time
import datetime



class RateLimiter:
    
    def __init__(self, debug: bool, limits: (int, int)=(10, 10), name: str = "") -> None:
        
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
        
    def __str__(self) -> str:
        return self.name+" : "+str(self.count)+" / "+str(self.limit)+" per "+str(self.duration)+" seconds"
    
    
    # Verify if the rate limiter is locked
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
        
    
    # Fired when a request is back
    async def get_back(self, num: int, timestamp: int, limit=None):
        async with self.back_lock:
            
            # If the current time window is up to date
            if self.time + self.duration > timestamp:
                
                if self.num == num:
                    self.currently_pending -= 1
                else:
                    self.previously_pending -= 1
                    self.count += 1
                    
            # Syncronize the beginning of the time window with server and update the limit
            if not self.synced:
                if not limit is None:
                    self.update_limit(limit)
                self.synced = True
                self.time = timestamp
                
            # If the time window is out of date
            else:
                await self._reset()
                if not limit is None:
                    self.update_limit(limit)
                self.previously_pending -= 1
                self.count += 1
                self.synced = True
                self.time = timestamp
    
    async def get_token(self):
        
        async with self.lock:
            
            # Check if outside the time window
            if self.time + self.duration < time.mktime(datetime.datetime.utcnow().timetuple()):
                
                # Wait until it's safe to request and open a new time window
                while self.previously_pending >= self.limit:
                    await asyncio.sleep(0.5)
                    
            # If in time window, check count
            elif self.count < self.limit:
                
                # Wait until it's safe to request or time window is over
                while (self.previously_pending + self.count) >= self.limit and self.time + self.duration > time.mktime(datetime.datetime.utcnow().timetuple()):
                    await asyncio.sleep(0.5)
            
            # If count limit reached, await for the end of the time window
            else:
                if self.debug:
                    print(self.name+" limit reached, sleeping for "+str( int((self.time + self.duration) - time.mktime(datetime.datetime.utcnow().timetuple())) + 1)+" seconds")
                    print("Limit : "+str(self.limit)+" per "+str(self.duration)+" / Count : "+ str(self.count))
                
                # Await for the next time window
                await asyncio.sleep(int((self.time + self.duration) - time.mktime(datetime.datetime.utcnow().timetuple())) + 1)
                
            
            async with self.back_lock:
                
                # Double check if a reset has not occured in the meantime
                timestamp = time.mktime(datetime.datetime.utcnow().timetuple())
                if self.time + self.duration < timestamp:
                    await self._reset()
                    
                
                # Increase count
                self.count += 1
                self.currently_pending += 1
                
                return self.num