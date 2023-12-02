import time
import threading
from summoner_profile.utils.exceptions import RateLimit

# API Requests
BURST_LIMIT = 20
BURST_TIME = 1
SUSTAINED_LIMIT = 100
SUSTAINED_TIME = 120

requests_ = []
lock = threading.Lock()

def rate_limiter(func):
    def wrapper(*args, **kwargs):
        global requests_
        while True:
            with lock:
                current_time = time.time()

                # Remove requests that are outside the sustained limit window
                requests_ = [req_time for req_time in requests_ if current_time - req_time < SUSTAINED_TIME]

                # Check if we can make a new request
                if len(requests_) >= SUSTAINED_LIMIT:
                    # If sustained limit reached, sleep until we can make a new request
                    sleep_time = SUSTAINED_TIME - (current_time - min(requests_)) + 0.1
                    print(f"Sustained limit reached, sleeping for {sleep_time} seconds")
                    for i in range(int(sleep_time), 0, -1):
                        print(f"Resuming in {i} seconds...")
                        time.sleep(1)
                    requests_.pop(0)

                # Check burst limit
                recent_requests = [req_time for req_time in requests_ if current_time - req_time < BURST_TIME]
                if len(recent_requests) >= BURST_LIMIT:
                    # If burst limit reached, sleep until we can make a new request
                    sleep_time = BURST_TIME - (current_time - min(recent_requests)) + 0.1
                    print(f"Burst limit reached, sleeping for {sleep_time} seconds")
                    for i in range(int(sleep_time), 0, -1):
                        print(f"Resuming in {i} seconds...")
                        time.sleep(1)
                    requests_.remove(min(recent_requests))

                requests_.append(time.time())

            try:
                return func(*args, **kwargs)
            except RateLimit as e:
                print(f"Rate limit exceeded, sleeping for {e.wait_for()} seconds")
                for i in range(e.wait_for(), 0, -1):
                    print(f"Resuming in {i} seconds...")
                    time.sleep(1)
    return wrapper