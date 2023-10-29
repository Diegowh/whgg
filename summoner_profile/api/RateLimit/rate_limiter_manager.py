from .rate_limiter import RateLimiter
from ..utils.utils import Singleton


class RateLimiterManager(metaclass=Singleton):
    
    def __init__(self, debug) -> None:
        
        PLATFORMS = ["br1","eun1","euw1","jp1","kr","la1", "la2","na1","oc1","tr1","ru"]
        REGIONS = ["americas","asia","europe","esports","ap","br","eu","kr","latam","na"]
        
        self.debug = debug
        
        self._rls = {server: RateLimiterServer(self.debug) for server in PLATFORMS + REGIONS}
        
    
    def on(self, server):
        return self._rls[server]


class RateLimiterServer:
    
    # Default application rate limit
    default_application_limits = [(20, 1), (100, 120)]
    
    default_methods_limits = {
        "get_champion_masteries":[(2000,60)],
        "get_champion_masteries_by_championId":[(2000,60)],
        "get_champion_masteries_score":[(2000,60)],
        "get_champion_rotations":[(30,10),(500,600)],
        "get_league_by_id":[(500,10)],
        "get_league_pages":[(50,10)],
        "get_league_position":[(300,60)],
        "get_challenger_league":[(30,10),(500,600)],
        "get_grandmaster_league":[(30,10),(500,600)],
        "get_master_league":[(30,10),(500,600)],
        "get_status":[(20000,10),(1200000,600)],
        "get_match":[(250,10)],
        "get_timeline":[(250,10)],
        "get_matchlist":[(500,10)],
        "get_current_game":[(20000,10),(1200000,600)],
        "get_featured_games":[(20000,10),(1200000,600)],
        "get_summoner":[(2000,60)],
        "get_summoner_by_accountId":[(2000,60)],
        "get_summoner_by_name":[(2000,60)],
        "get_summoner_by_puuId":[(2000,60)],
        "get_third_party_code":[(500,60)],
        "register_provider":[(10,10),(500,600)],
        "register_tournament":[(30,10),(500,600)],
        "create_tournament_code":[(30,10),(500,600)],
        "get_lobby_events":[(30,10),(500,600)],
        "get_clash_tournaments":[(10,60)],
        "get_clash_tournament_by_id":[(10,60)],
        "get_clash_tournament_by_teamId":[(200,60)],
        "get_clash_team_by_id":[(200,60)],
        "get_clash_players_by_summonerId":[(200,60)],
        "get_tft_league_by_id":[(100,10)],
        "get_tft_league_pages":[(50,10)],
        "get_tft_league_position":[(300,60)],
        "get_tft_challenger_league":[(30,10),(500,600)],
        "get_tft_grandmaster_league":[(30,10),(500,600)],
        "get_tft_master_league":[(30,10),(500,600)],
        "get_tft_match":[(200,10)],
        "get_tft_matchlist":[(400,10)],
        "get_tft_summoner":[(2000,60)],
        "get_tft_summoner_by_accountId":[(2000,60)],
        "get_tft_summoner_by_name":[(2000,60)],
        "get_tft_summoner_by_puuId":[(2000,60)],
        "get_account_by_puuId":[(1000,60)],
        "get_account_by_riotId":[(1000,60)],
        "get_active_shards":[(20000,10),(1200000,600)],
        "get_lor_leaderboard":[(30,10),(500,600)],
        "get_lor_match":[(100,3600)],
        "get_lor_matchlist":[(200,3600)],
        "get_valorant_content":[(60,60)],
        "get_valorant_match":[(60,60)],
        "get_valorant_matchlist":[(120,60)],
        "get_valorant_recent_matches":[(60,60)],
        "get_valorant_leaderboard":[(10,10)]
    }
    
    
    def __init__(self, debug) -> None:
        
        self.debug = debug
        
        self.application = []
        
        for app_limit in self.default_application_limits:
            self.application.append(RateLimiter(self.debug, app_limit, "App"))
            
        self.methods = {}
        
        for method in self.default_methods_limits:
            
            self.methods[method] = []
            
            for method_limit in self.default_methods_limits[method]:
                self.methods[method].append(RateLimiter(self.debug, method_limit, method))
                
                
    def __str__(self):
        
        result = "Rate limits: \n"
        
        for app_limit in self.application:
            result += "\t" + str(app_limit) + "\n"
            
        for method in self.methods:
            for method_limit in self.methods[method]:
                result += "\t" + str(method_limit) + "\n"
                
        return result
    
    def locked(self) -> bool:
        return any([app_limit.locked() for app_limit in self.application] + [method_limit.locked() for method in self.methods for method_limit in self.methods[method]])
    
    
    def update_application_limit(self, duration: int, limit: int):
        for app_limit in self.application:
            if duration == app_limit.get_duration():
                app_limit.update_limit(limit)
                return
    
        self.application.append(RateLimiter(self.debug, (limit, duration), "App"))
        

    def delete_application_limit(self, duration: int):
        for app_limit in self.application:
            if duration == app_limit.get_duration():
                self.application.remove(app_limit)
                return # To avoid unnecesary iterations
            
    def display_application_limit(self):
        for app_limit in self.application:
            print(str(app_limit.get_limit()) + " : " + str(app_limit.get_duration()))

    def update_methods_limit(self, method: str, duration: int, limit: int):
        
        if method in self.methods:
            for method_limit in self.methods[method]:
                if duration == method_limit.get_duration():
                    method_limit.update_limit(limit)
                    return 

            self.methods[method].append(RateLimiter(self.debug, (limit, duration), method))
            
        else:
            self.methods[method] = []
            self.methods[method].append(RateLimiter(self.debug, (limit, duration), method))

    def delete_methods_limit(self, method: str, duration:int):
        for method_limit in self.methods[method]:
            if duration == method_limit.get_duration():
                self.methods[method].remove(method_limit)
                return
            
    async def get_back(self, method: str, token, timestamp: int, limits):
        #TODO Refactor this method to follow single responsibility principle
        if limits is None:
            for i, app_limit in enumerate(self.application):
                await app_limit.get_back(token[0][i], timestamp)
            
            for i, method_limit in enumerate(self.methods[method]):
                await method_limit.get_back(token[1][i])
        
        else:
            app_limits_to_delete = []
            method_limis_to_delete = []
            
            for i, app_limit in enumerate(self.application):
                
                if app_limit.get_duration() in limits[0]:
                    await app_limit.get_back(token[0][i], timestamp, limits[0][app_limit.get_duration()])
                    del(limits[0][app_limit.get_duration()])
                
                else:
                    # If the limit is not in the returned header, its considered out of date, so queue to delete it
                    app_limits_to_delete.append(app_limit.get_duration())
                    
            # Delete the out of date app limits
            for i in app_limits_to_delete:
                self.delete_application_limit(i)
                
            for duration in limits[0]:
                # If the limit exists in the returned header but not in the manager, create it
                self.update_application_limit(duration, limits[0][duration])
                
            for i, method_limit in enumerate(self.methods[method]):
                if method_limit.get_duration() in limits[1]:
                    await method_limit.get_back(token[1][i], timestamp, limits[1][method_limit.get_duration()])
                    del(limits[1][method_limit.get_duration()])
                
                else:
                    # If the limit is not in the returned header, its considered out of date, so queue to delete it
                    method_limis_to_delete.append(method_limit.get_duration())
            
            
            # Delete the out of date method limits
            for i in method_limis_to_delete:
                self.delete_methods_limit(method, i)
                
            for duration in limits[1]:
                # If the limit exists in the returned header but not in the manager, create it
                self.update_methods_limit(method, duration, limits[1][duration])

                for method_limit in self.methods[method]:
                    if duration == method_limit.get_duration():
                        method_limit.count += 1
                        return
    
    def display_method_limits(self):
        for method in self.methods:
            print(method)
            
            for method_limit in self.methods[method]:
                print(str(method_limit.get_limit()) + " : " + str(method_limit.get_duration()))    
        print()

    async def get_token(self, method: str):
        
        app_token = []
        method_token = []
        
        for app_limit in self.application:
            app_token.append(await app_limit.get_token())
        
        if not method in self.methods:
            self.update_methods_limit(method, 10, 20000)
        
        for method_limit in self.methods[method]:
            method_token.append(await method_limit.get_token())
        
        return (app_token, method_token)
        