from datetime import datetime
import time
import re

from .api_client import ApiClient
from .db_manager import DbManager

from summoner_profile.utils.utils import (
    hours_to_seconds,
    calculate_kda,
)
from asgiref.sync import async_to_sync
from summoner_profile.utils.dataclasses import (
    SummonerData,
    RankedStatsData,
    ChampionStatsData,
    MatchData,
    ParticipantData,
    RequestData
)



class DataManager:
    
    HOURS_BEFORE_UPDATING_DATABASE = 1.5
    SECONDS_BEFORE_UPDATING_DATABASE = hours_to_seconds(hours=HOURS_BEFORE_UPDATING_DATABASE)
    
    
    def __init__(self, request: RequestData) -> None:
        
        self._request = request
        
        self._api_client = ApiClient(server=self.request.server, debug=True)
        self._db_manager = DbManager()
        
        # Pide los datos al inicializar la clase para obtener el puuid y el id
        self._summoner_data: SummonerData = self._create_summoner_data(summoner_name=self.summoner_name)
        
        self._puuid = self._summoner_data.puuid
        self._id = self._summoner_data.id 
    
    @property
    def request(self):
        return self._request
    
    @property
    def api_client(self):
        return self._api_client
    
    @property
    def db_manager(self):
        return self._db_manager
    
    @property
    def summoner_data(self):
        return self._summoner_data
    
    @property
    def puuid(self):
        return self._puuid
    
    @property
    def id(self):
        return self._id
    
    
    def get_requested_data(self):
        
        # Si el puuid existia en la base de datos 
        if self.db_manager.is_puuid_in_database():
            
            # Si es el momento de actualizar en base al tiempo desde la ultima actualizacion
            if self.is_time_to_update():
                
                # Pide los datos a la API de Riot y los guarda en la base de datos
                pass
            
            # Si no es el momento de actualizar, obtiene los datos de la base de datos directamente
            else: 
                pass
                
        # Si el puuid no existia en la base de datos previamente
        else:
            # Pide los datos a la API de Riot y los guarda en la base de datos
            pass
    
    def is_time_to_update(self) -> bool:
        '''
        Comprueba si ha pasado el tiempo suficiente desde la ultima actualizacion de la base de datos
        '''
        now = int(time.time())
        last_update = self.db_manager.last_update()
        
        return (now - last_update) > self.SECONDS_BEFORE_UPDATING_DATABASE
    
    
    # Se encarga de obtener los datos de la Api de Riot y crea un objeto SummonerData
    def _create_summoner_data(self) -> SummonerData:
        response = async_to_sync(self.api_client.get_summoner_by_name)(
                    summoner_name=self.summoner_name
                    )
        
        summoner_data = SummonerData(
            puuid=response["puuid"],
            id=response["id"],
            name=response["name"],
            icon_id=response["profileIconId"],
            summoner_level=response["summonerLevel"],
            last_update=response["revisionDate"]
        )
        return summoner_data
                
                
    def _create_ranked_stats_data_list(self) -> list[RankedStatsData]:
        response: list = async_to_sync(self.api_client.get_league_by_summoner)(
                summoner_id=self.id
                )
        
        ranked_stats_list = []
        
        for queue in response:
            
            ranked_stats_data = RankedStatsData(
                queue_type=queue["queueType"],
                tier=queue["tier"],
                rank=queue["rank"],
                league_points=queue["leaguePoints"],
                wins=queue["wins"],
                losses=queue["losses"],
                winrate=queue["wins"] / (queue["wins"] + queue["losses"]), # TODO: Crea una función para calcular el winrate
                summoner=self.puuid
            )
            ranked_stats_list.append(ranked_stats_data)
        
        return ranked_stats_list
        
    def _create_match_data_list(self) -> list[MatchData]:
        
        all_match_data: list[MatchData] = []
        
        for match_id in self._all_match_ids():
            
            match_data_response = async_to_sync(self.api_client.get_match)(match_id=match_id)
            
            match_data, all_participant_data = self.filter_match_response(match_data_response=match_data_response)

            all_match_data.append(match_data)
            
        
        return all_match_data
            
            

    def _all_match_ids(self) -> list[str]:
        MAX_MATCHES = 5000 # Por poner un limite a la cantidad de partidas que se pidan
        REQUEST_CAP = 100 # La API solo permite pedir de 100 en 100
        season_start = int(datetime(2023, 1, 14).timestamp()) # TODO: Obtener esta fecha de la base de datos
        
        match_ids = []
        params = {
            "startTime": season_start,
            "type": "ranked",
        }
        
        for start_index in range(0, MAX_MATCHES, REQUEST_CAP):
            
            params["start"] = start_index
            params["count"] = int(min(REQUEST_CAP, MAX_MATCHES - start_index)) # Para evitar pedir más partidas de las que se pueden
            
            matchlist_response: list = async_to_sync(self.api_client.get_matchlist)(
                puuid=self.puuid,
                params= params,
                )
            
            if matchlist_response == []:
                break
            
            match_ids += matchlist_response
        
        return match_ids
        
    def _create_participant_data(self, participant, match_id):
        return ParticipantData(
            puuid = participant["puuid"],
            name = participant["summonerName"],
            champion_name = participant["championName"],
            team_id = participant["teamId"],
            match = match_id,
        )
        
    def _create_match_data(self, match_data_response) -> MatchData:
        return MatchData(
            id = match_data_response["metadata"]["matchId"],
            game_start = match_data_response["info"]["gameStartTimestamp"],
            game_end = match_data_response["info"]["gameEndTimestamp"],
            game_duration = match_data_response["info"]["gameDuration"],
            game_mode = match_data_response["info"]["gameMode"],
            game_type = match_data_response["info"]["gameType"],
            
            )
        
    def _fill_match_data(self, match_data: MatchData, participant) -> MatchData:
        '''
        Completa los datos de la instancia de MatchData con los datos del participante
        '''
        
        match_data.champion_played = participant["championName"]
        match_data.win = participant["win"]
        match_data.kills = participant["kills"]
        match_data.deaths = participant["deaths"]
        match_data.assists = participant["assists"]
        
        match_data.kda =  calculate_kda(
            kills=participant["kills"],
            deaths=participant["deaths"],
            assists=participant["assists"],
        )
        
        match_data.minion_kills = sum(
            participant["totalMinionsKilled"],
            participant["neutralMinionsKilledTeamJungle"],
            participant["neutralMinionsKilledEnemyJungle"],
        )
        
        match_data.vision_score = participant["visionScore"]
        match_data.team_position = participant["teamPosition"]
        match_data.team_id = participant["teamId"]
        match_data.summoner = self.puuid
        match_data.item_purchase = [participant[f"item{i}"] for i in range(7)]
        match_data.summoner_spells = [participant[f"summoner{i}Id"] for i in range(1, 3)]
    
    
    def filter_match_response(self, match_data_response) -> tuple[MatchData, list[ParticipantData]]:
        '''
        Recibe una la respuesta de la API de Riot con los datos de una partida y devuelve una instancia de MatchData y una lista de ParticipantData
        '''
        # Crea una instancia de MatchData con los datos referentes al match
        match_data = self._create_match_data(match_data_response)
        
        # Obtiene una lista con los datos de todos los participantes
        all_participants: list[dict] = match_data_response["info"]["participants"]
        
        filtered_participant_data: list[ParticipantData] = []
        
        for participant in all_participants:
            
            # Si el puuid del participante es el del summoner, son los datos de este.
            if participant["puuid"] == self.puuid:
                
                # Completa los datos de la instancia de MatchData con los datos del participante
                self._fill_match_data(match_data=match_data, participant=participant)
            
            participant_data = self._create_participant_data(participant=participant, match_id=match_data.id)
            
            filtered_participant_data.append(participant_data)
            
        return match_data, filtered_participant_data


    # TODO Refactorizar esta funcion
    def last_matches_data(self, amount: int = 20):
            
        # Get the match ids
        match_ids = self._all_match_ids()
        
        # Get the match data
        matches_data = self.matches_data(match_ids=match_ids)
        
        # Ensure amount is not greater than the number of matches
        amount = min(amount, len(match_ids))
        
        formatted_matches_data = [self.data_manager.filter_match(match_data=matches_data[i]) for i in range(amount)]
        
        return formatted_matches_data