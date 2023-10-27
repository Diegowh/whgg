class Singleton(type):
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        
        return cls._instances[cls]
    
    
def getLimits(headers):
    if 'X-Method-Rate-Limit' in headers and 'X-App-Rate-Limit' in headers:
        appLimits = {}
        for appLimit in headers['X-App-Rate-Limit'].split(","):
            appLimits[int(appLimit.split(":")[1])] = int(appLimit.split(":")[0])

        methodLimits = {}
        for methodLimit in headers['X-Method-Rate-Limit'].split(","):
            methodLimits[int(methodLimit.split(":")[1])] = int(methodLimit.split(":")[0])

        return (appLimits,methodLimits)
    return None