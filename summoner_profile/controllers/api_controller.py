from summoner_profile.utils.env_loader import EnvLoader
from summoner_profile.utils import exceptions as exc
from summoner_profile.utils.decorators import exceptions
from summoner_profile.utils import utils
from summoner_profile.utils.rate_limiter import rate_limiter

import requests
import json


class ApiController:
    BASE_URL = "https://{server}.api.riotgames.com/"
    BASE_URL_LOL = BASE_URL + "lol/"
    BASE_URL_TFT = BASE_URL + "tft/"
    BASE_URL_VAL = BASE_URL + "val/"
    BASE_URL_LOR = BASE_URL + "lor/"
    BASE_URL_RIOT = BASE_URL + "riot/"

    PLATFORMS = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru", "sg2", "th2", "tw2",
                 "vn2"]
    REGIONS = ["americas", "asia", "europe", "esports",
               "ap", "br", "eu", "kr", "latam", "na", "sea"]
    PLATFORMS_TO_REGIONS = {"br1": "americas", "eun1": "europe", "euw1": "europe", "jp1": "asia", "kr": "asia",
                            "la1": "americas", "la2": "americas", "na1": "americas", "oc1": "sea", "tr1": "europe",
                            "ru": "europe", "sg2": "sea", "th2": "sea", "tw2": "sea", "vn2": "sea"}
    TOURNAMENT_REGIONS = "americas"

    def __init__(self, server: str, auto_retry: bool = False, debug: bool = False) -> None:

        # Obtiene la ApiKey del .env
        env_loader = EnvLoader()
        try:
            self._key = env_loader.get("RIOT_API_KEY")
        except EnvironmentError:
            raise exc.RiotApiKeyNotFound

        self.set_server(server)

        self._auto_retry = auto_retry
        self._debug = debug

    def set_server(self, server):
        if server in self.PLATFORMS:
            self.set_platform(server)
        elif server in self.REGIONS:
            self.set_region(server)
        else:
            raise exc.InvalidServer(server, self.PLATFORMS + self.REGIONS)

    def set_platform(self, platform):
        if platform in self.PLATFORMS:
            self._platform = platform
            self._region = self.PLATFORMS_TO_REGIONS[platform]
        else:
            raise exc.InvalidServer(platform, self.PLATFORMS)

    def set_region(self, region):
        if region in self.REGIONS:
            self._platform = None
            self._region = region
        else:
            raise exc.InvalidServer(region, self.REGIONS)

    @rate_limiter
    @exceptions
    def fetch(self, url, method="GET", data=None):

        headers = {
            "X-Riot-Token": self._key
        }

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            else:
                response = requests.request(
                    method, url, headers=headers, data=json.dumps(data))

        # Por si hay un timeout
        except Exception as e:
            print(e)
            return None

        return response

    # Champion Mastery
    def get_champion_masteries(self, summoner_id: str):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getAllChampionMasteries
        """
        return self.fetch(
            (self.BASE_URL_LOL + "champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}").format(
                server=self._platform, summoner_id=summoner_id))

    def get_champion_masteries_by_champion_id(self, summoner_id, champion_id):
        """
        :param string summoner_id: summoner_id of the player
        :param int championId: id of the champion

        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMastery
        """
        return self.fetch((
            self.BASE_URL_LOL + "champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}").format(
            server=self._platform, summonerId=summoner_id, championId=champion_id))

    def get_champion_masteries_score(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/api-methods/#champion-mastery-v4/GET_getChampionMasteryScore
        """
        return self.fetch(
            (self.BASE_URL_LOL + "champion-mastery/v4/scores/by-summoner/{summoner_id}").format(server=self._platform,
                                                                                                summoner_id=summoner_id))

    # Champion rotations
    def get_champion_rotations(self):
        """
        Returns the result of https://developer.riotgames.com/api-methods/#champion-v3/GET_getChampionInfo
        """
        return self.fetch((self.BASE_URL_LOL + "platform/v3/champion-rotations").format(server=self._platform))

    # League
    def get_league_by_summoner(self, summoner_id):
        """
        :param string summoner_id: id of the summoner

        Returns the result of https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesForSummoner
        """
        return self.fetch(
            (self.BASE_URL_LOL + "league/v4/entries/by-summoner/{summoner_id}").format(server=self._platform,
                                                                                       summoner_id=summoner_id))

    def get_league_by_id(self, league_id):
        """
        :param string league_id: id of the league

        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueById
        """
        return self.fetch(
            (self.BASE_URL_LOL + "league/v4/leagues/{league_id}").format(server=self._platform, league_id=league_id))

    def get_league_pages(self, queue="RANKED_SOLO_5X5", tier="DIAMOND", division="I", page=1):
        """
        :param string queue: queue to get the page of
        :param string tier: tier to get the page of
        :param string division: division to get the page of
        :param int page: page to get

        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueEntriesForSummoner
        """
        return self.fetch((self.BASE_URL_LOL + "league/v4/entries/{queue}/{tier}/{division}?page={page}").format(
            server=self._platform, queue=queue, tier=tier, division=division, page=page))

    def get_challenger_league(self, queue="RANKED_SOLO_5x5"):
        """
        :param string queue: queue to get the challenger league of
            Values accepted : 
             * RANKED_SOLO_5x5 *(default)*
             * RANKED_FLEX_SR

        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getChallengerLeague
        """
        return self.fetch(
            (self.BASE_URL_LOL + "league/v4/challengerleagues/by-queue/{queue}").format(server=self._platform,
                                                                                        queue=queue))

    def get_grandmaster_league(self, queue="RANKED_SOLO_5x5"):
        """
        :param string queue: queue to get the master league of
            Values accepted : 
             * RANKED_SOLO_5x5 *(default)*
             * RANKED_FLEX_SR

        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getGrandmasterLeague
        """
        return self.fetch(
            (self.BASE_URL_LOL + "league/v4/grandmasterleagues/by-queue/{queue}").format(server=self._platform,
                                                                                         queue=queue))

    def get_master_league(self, queue="RANKED_SOLO_5x5"):
        """
        :param string queue: queue to get the master league of
            Values accepted : 
             * RANKED_SOLO_5x5 *(default)*
             * RANKED_FLEX_SR

        Returns the result of https://developer.riotgames.com/api-methods/#league-v4/GET_getMasterLeague
        """
        return self.fetch(
            (self.BASE_URL_LOL + "league/v4/masterleagues/by-queue/{queue}").format(server=self._platform, queue=queue))

    # Status
    def get_status(self):
        """
        Returns the result of https://developer.riotgames.com/apis#lol-status-v4/GET_getPlatformData
        """
        return self.fetch((self.BASE_URL_LOL + "status/v4/platform-data").format(server=self._platform))

    # Match
    def get_match(self, match_id):
        """
        :param int match_id: match_id of the match, also known as gameId

        Returns the result of https://developer.riotgames.com/apis#match-v5/GET_getMatch
        """
        return self.fetch(
            (self.BASE_URL_LOL + "match/v5/matches/{match_id}").format(server=self._region, match_id=match_id))

    def get_timeline(self, match_id):
        """
        :param int match_id: match_id of the match, also known as gameId

        Returns the result of https://developer.riotgames.com/apis#match-v5/GET_getTimeline
        """
        return self.fetch(
            (self.BASE_URL_LOL + "match/v5/matches/{match_id}/timeline").format(server=self._region, match_id=match_id))

    def get_matchlist(self, puuid, params=None):
        """
        :param string puuid: puuid of the player
        :param object params: all key:value params to add to the request

        Returns the result of https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID
        """
        return self.fetch(
            (self.BASE_URL_LOL + "match/v5/matches/by-puuid/{puuid}/ids{params}").format(server=self._region,
                                                                                         puuid=puuid,
                                                                                         params=utils.url_params(
                                                                                             params)))

    # Spectator
    def get_current_game(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/api-methods/#spectator-v4/GET_getCurrentGameInfoBySummoner
        """
        return self.fetch(
            (self.BASE_URL_LOL + "spectator/v4/active-games/by-summoner/{summoner_id}").format(server=self._platform,
                                                                                               summoner_id=summoner_id))

    def get_featured_games(self):
        """
        Returns the result of https://developer.riotgames.com/api-methods/#spectator-v3/GET_getFeaturedGames
        """
        return self.fetch((self.BASE_URL_LOL + "spectator/v4/featured-games").format(server=self._platform))

    # Summoner
    def get_summoner(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerId
        """
        return self.fetch((self.BASE_URL_LOL + "summoner/v4/summoners/{summoner_id}").format(server=self._platform,
                                                                                             summoner_id=summoner_id))

    def get_summoner_by_account_id(self, account_id):
        """
        :param string account_id: account_id of the player

        Returns the result of https://developer.riotgames.com/api-methods/#summoner-v4/GET_getByAccountId
        """
        return self.fetch(
            (self.BASE_URL_LOL + "summoner/v4/summoners/by-account/{account_id}").format(server=self._platform,
                                                                                         account_id=account_id))

    def get_summoner_by_name(self, summoner_name):
        """
        :param string summoner_name: name of the player

        Returns the result of https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName
        """
        return self.fetch(
            (self.BASE_URL_LOL + "summoner/v4/summoners/by-name/{summoner_name}").format(server=self._platform,
                                                                                         summoner_name=summoner_name))

    def get_summoner_by_puuid(self, puuid):
        """
        :param string puuid: puuid of the player

        Returns the result of https://developer.riotgames.com/apis#summoner-v4/GET_getByPUUID
        """
        return self.fetch(
            (self.BASE_URL_LOL + "summoner/v4/summoners/by-puuid/{puuid}").format(server=self._platform, puuid=puuid))

    # TFT
    def get_tft_league_by_id(self, league_id):
        """
        :param string league_id: id of the league

        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getLeagueById
        """
        return self.fetch(
            (self.BASE_URL_TFT + "league/v1/leagues/{league_id}").format(server=self._platform, league_id=league_id))

    def get_tft_league_pages(self, tier="DIAMOND", division="I", page=1):
        """
        :param string tier: tier to get the page of
        :param string division: division to get the page of
        :param int page: page to get

        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getLeagueEntries
        """
        return self.fetch(
            (self.BASE_URL_TFT + "league/v1/entries/{tier}/{division}?page={page}").format(server=self._platform,
                                                                                           tier=tier, division=division,
                                                                                           page=page))

    def get_tft_league_position(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getLeagueEntriesForSummoner
        """
        return self.fetch(
            (self.BASE_URL_TFT + "league/v1/entries/by-summoner/{summoner_id}").format(server=self._platform,
                                                                                       summoner_id=summoner_id))

    def get_tft_challenger_league(self):
        """
        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getChallengerLeague
        """
        return self.fetch((self.BASE_URL_TFT + "league/v1/challenger").format(server=self._platform))

    def get_tft_grandmaster_league(self):
        """
        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getGrandmasterLeague
        """
        return self.fetch((self.BASE_URL_TFT + "league/v1/grandmaster").format(server=self._platform))

    def get_tft_master_league(self):
        """
        Returns the result of https://developer.riotgames.com/apis#tft-league-v1/GET_getMasterLeague
        """
        return self.fetch((self.BASE_URL_TFT + "league/v1/master").format(server=self._platform))

    def get_tft_match(self, match_id):
        """
        :param string match_id: match_id of the match, also known as game_id

        Returns the result of https://developer.riotgames.com/api-methods/#match-v4/GET_getMatch
        """
        return self.fetch(
            (self.BASE_URL_TFT + "match/v1/matches/{match_id}").format(server=self._region, match_id=match_id))

    def get_tft_matchlist(self, puuid, params=None):
        """
        :param string puuid: puuid of the player
        :param object params: all key:value params to add to the request

        Returns the result of https://developer.riotgames.com/apis#tft-match-v1/GET_getMatchIdsByPUUID
        """
        return self.fetch(
            (self.BASE_URL_TFT + "match/v1/matches/by-puuid/{puuid}/ids{params}").format(server=self._region,
                                                                                         puuid=puuid,
                                                                                         params=utils.url_params(
                                                                                             params)))

    def get_tft_summoner(self, summoner_id):
        """
        :param string summoner_id: summoner_id of the player

        Returns the result of https://developer.riotgames.com/apis#tft-summoner-v1/GET_getBySummonerId
        """
        return self.fetch((self.BASE_URL_TFT + "summoner/v1/summoners/{summoner_id}").format(server=self._platform,
                                                                                             summoner_id=summoner_id))

    def get_tft_summoner_by_account_id(self, account_id):
        """
        :param string account_id: account_id of the player

        Returns the result of https://developer.riotgames.com/apis#tft-summoner-v1/GET_getByAccountId
        """
        return self.fetch(
            (self.BASE_URL_TFT + "summoner/v1/summoners/by-account/{account_id}").format(server=self._platform,
                                                                                         account_id=account_id))

    def get_tft_summoner_by_puuid(self, puuid):
        """
        :param string puuid: puuid of the player

        Returns the result of https://developer.riotgames.com/apis#tft-summoner-v1/GET_getByPUUID
        """
        return self.fetch(
            (self.BASE_URL_TFT + "summoner/v1/summoners/by-puuid/{puuid}").format(server=self._platform, puuid=puuid))

    def get_tft_summoner_by_name(self, summoner_name):
        """
        :param string summoner_name: name of the player

        Returns the result of https://developer.riotgames.com/apis#tft-summoner-v1/GET_getBySummonerName
        """
        return self.fetch(
            (self.BASE_URL_TFT + "summoner/v1/summoners/by-name/{summoner_name}").format(server=self._platform,
                                                                                         summoner_name=summoner_name))

    # Riot endpoints
    def get_account_by_puuid(self, puuid):
        """
        :param string puuid: puuid of the player

        Returns the result of https://developer.riotgames.com/apis#account-v1/GET_getByPuuid
        """
        return self.fetch(
            (self.BASE_URL_RIOT + "account/v1/accounts/by-puuid/{puuid}").format(server=self._region, puuid=puuid))

    def get_account_by_riot_id(self, game_name, tag_line):
        """
        :param string game_name: name of the player
        :param string tag_line: tag of the player

        Returns the result of https://developer.riotgames.com/apis#account-v1/GET_getByRiotId
        """
        print(f"El game name en ApiController es: {game_name}")
        url = (self.BASE_URL_RIOT + "account/v1/accounts/by-riot-id/{game_name}/{tag_line}").format(
            server=self._region, game_name=game_name, tag_line=tag_line)

        print(f"La url es: {url}")
        return self.fetch(
            url=url)

    def get_active_shards(self, puuid, game):
        """
        :param string puuid: puuid of the player
        :param string game: targeted game ("val" or "lor")

        Returns the result of https://developer.riotgames.com/apis#account-v1/GET_getActiveShard
        """
        return self.fetch((self.BASE_URL_RIOT + "account/v1/active-shards/by-game/{game}/by-puuid/{puuid}").format(
            server=self._region, game=game, puuid=puuid))

    # Valorant
    def get_valorant_content(self, locale=None):
        """
        :param string locale: language return. Default to None

        Returns the result of https://developer.riotgames.com/apis#val-content-v1/GET_getContent
        """
        return self.fetch((self.BASE_URL_VAL + "content/v1/contents{locale}").format(server=self._region,
                                                                                     locale="?locale=" + locale if locale is not None else ""))

    def get_valorant_match(self, match_id):
        """
        :param string match_id: id of the match

        Returns the result of https://developer.riotgames.com/apis#val-match-v1/GET_getMatch
        """
        return self.fetch(
            (self.BASE_URL_VAL + "match/v1/matches/{match_id}").format(server=self._region, match_id=match_id))

    def get_valorant_matchlist(self, puuid):
        """
        :param string puuid: puuid of the player

        Returns the result of https://developer.riotgames.com/apis#val-match-v1/GET_getMatchlist
        """
        return self.fetch(
            (self.BASE_URL_VAL + "match/v1/matchlists/by-puuid/{puuid}").format(server=self._region, puuid=puuid))

    def get_valorant_recent_matches(self, queue):
        """
        :param string queue: queue of the matches

        Returns the result of https://developer.riotgames.com/apis#val-match-v1/GET_getRecent
        """
        return self.fetch(
            (self.BASE_URL_VAL + "match/v1/recent-matches/by-queue/{queue}").format(server=self._region, queue=queue))

    def get_valorant_leaderboard(self, act_id, size=200, start_index=0):
        """
        :param string act_id: id of the act for the leaderboards
        :param int size: size of the leaderboard list
        :param int start_index: index to start the leaderboard list

        Returns the result of https://developer.riotgames.com/apis#val-ranked-v1/GET_getLeaderboard
        """
        return self.fetch(
            (self.BASE_URL_VAL + "ranked/v1/leaderboards/by-act/{act_id}?size={}size&startIndex={start_index}").format(
                server=self._region, act_id=act_id, size=size, start_index=start_index))
