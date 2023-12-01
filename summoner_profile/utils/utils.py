import time
import datetime

class Singleton(type):
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        
        return cls._instances[cls]
    
    
def get_limits(headers):
    if 'X-Method-Rate-Limit' in headers and 'X-App-Rate-Limit' in headers:
        appLimits = {}
        for appLimit in headers['X-App-Rate-Limit'].split(","):
            appLimits[int(appLimit.split(":")[1])] = int(appLimit.split(":")[0])

        methodLimits = {}
        for methodLimit in headers['X-Method-Rate-Limit'].split(","):
            methodLimits[int(methodLimit.split(":")[1])] = int(methodLimit.split(":")[0])

        return (appLimits,methodLimits)
    return None

def date_to_timestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').timetuple()))

def url_params(params):
    if params is None:
        return ""
    else:
        strParams = "?"
        for i in params:
            if type(params[i]) == list:
                for p in params[i]:
                    strParams+= i+"="+str(p)+"&"
            else:
                strParams+= i+"="+str(params[i])+"&"
        return strParams[:-1]


def get_timestamp(headers):
    try:
        timestamp = date_to_timestamp(headers['Date'])
    except Exception as e:
        timestamp = int(time.time())
    return timestamp


def hours_to_seconds(hours):
    return hours * 60 * 60


def calculate_kda(kills, deaths, assists):
    if deaths == 0:
        deaths = 1 # Para evitar que se divida por 0 y siga devolviendo float
    return round((kills + assists / deaths), 2)