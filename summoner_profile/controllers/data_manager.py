from datetime import datetime
import time
from django import conf

from django.conf import settings

from .db_manager import DbManager
from .api_controller import ApiController

from summoner_profile.utils.utils import (
    hours_to_seconds,
    calculate_kda,
    league_winrate,
)

from asgiref.sync import async_to_sync
from summoner_profile.utils.dataclasses import (
    SummonerData,
    RankedStatsData,
    ChampionStatsData,
    MatchData,
    ParticipantData,
    RequestData,
    ResponseData
)


class DataManager:

    def __init__(self, request: RequestData) -> None:

        self._request = request

        self._api_controller = ApiController(
            server=self.request.server, debug=True)

        # Pide los datos al inicializar la clase para obtener el puuid y el id
        self._summoner_data: SummonerData = self._get_summoner_data_from_api(
            game_name=self.request.game_name, tagline=self.request.tagline)

        self._puuid = self._summoner_data.puuid
        self._id = self._summoner_data.id

        self._db_manager = DbManager(puuid=self.puuid)

        self._matches_data = []
        self._participants_data = []

        self.seconds_before_updating_database = int(
            hours_to_seconds(hours=settings.HOURS_BEFORE_UPDATING_DATABASE))

    @property
    def request(self):
        return self._request

    @property
    def api_controller(self):
        return self._api_controller

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

    @property
    def matches_data(self):
        return self._matches_data

    @property
    def participants_data(self):
        return self._participants_data

    def get_response_data(self) -> ResponseData:

        # Comprueba si hace falta actualizar la base de datos antes de devolver los datos
        if self.db_manager.is_puuid_in_database() and not self.is_time_to_update():
            print("El puuid ya existia, y no hace falta actualizar")
            response_data = self.db_manager.fetch_response_data()
            return response_data

        # Solicita los datos requeridos a la API de Riot y los actualiza en la base de datos
        self.db_manager.update_summoner(data=self.summoner_data)
        ranked_stats_data_list = self._get_ranked_stats_list_from_api()
        self.db_manager.update_ranked_stats(data=ranked_stats_data_list)
        self._get_match_and_participant_data_from_api()
        self.db_manager.update_match_data(data=self.matches_data)
        self.db_manager.update_participants_data(data=self.participants_data)
        self.db_manager.update_champion_stats()

        # Construye el objeto ResponseData
        response_data = self.db_manager.fetch_response_data()

        return response_data

    def is_time_to_update(self) -> bool:
        '''
        Comprueba si ha pasado el tiempo suficiente desde la ultima actualizacion de la base de datos
        '''
        now = int(time.time())
        last_update = self.db_manager.last_update()

        if last_update is None:
            return True

        print(
            f"Ha pasado: {now - last_update} segundos desde la ultima actualizacion")

        return (now - last_update) > self.seconds_before_updating_database

    def _get_summoner_data_from_api(self, game_name: str, tagline: str) -> SummonerData:
        print("El Game name en el data manager es: " + game_name)
        riot_acc_response = self.api_controller.get_account_by_riot_id(
            game_name=game_name,
            tag_line=tagline,
        )

        summ_response = self.api_controller.get_summoner_by_puuid(
            puuid=riot_acc_response["puuid"],
        )

        summoner_data = SummonerData(
            puuid=riot_acc_response["puuid"],
            id=summ_response["id"],
            # Por ahora lo dejo asi, en el futuro mejorare esto
            name=riot_acc_response["gameName"] + \
            "#" + riot_acc_response["tagLine"],
            icon_id=summ_response["profileIconId"],
            summoner_level=summ_response["summonerLevel"],
            last_update=int(time.time()),
        )
        return summoner_data

    def _get_ranked_stats_list_from_api(self) -> list[RankedStatsData]:
        response: list = self.api_controller.get_league_by_summoner(
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
                winrate=league_winrate(
                    wins=queue["wins"], losses=queue["losses"]),
            )
            ranked_stats_list.append(ranked_stats_data)

        return ranked_stats_list

    def _get_match_and_participant_data_from_api(self) -> None:

        all_match_data: list[MatchData] = []
        all_participant_data: list[ParticipantData] = []

        for match_id in self._all_match_ids():
            match_data_response = self.api_controller.get_match(
                match_id=match_id)

            match_data, participant_data = self.filter_match_response(
                match_data_response=match_data_response)

            all_match_data.append(match_data)
            all_participant_data += participant_data

        self._matches_data = all_match_data
        self._participants_data = all_participant_data

    def _all_match_ids(self) -> list[str]:
        # TODO: Obtener esta fecha de la base de datos
        season_start = int(datetime(2023, 1, 14).timestamp())

        match_ids = []
        params = {
            "startTime": season_start,
            "type": "ranked",
        }

        for start_index in range(0, settings.MAX_MATCH_IDS_REQUESTED, settings.RIOT_API_REQUEST_CAP):

            params["start"] = start_index
            # Para evitar pedir más partidas de las que se pueden
            params["count"] = int(
                min(settings.RIOT_API_REQUEST_CAP, settings.MAX_MATCH_IDS_REQUESTED - start_index))

            matchlist_response: list = self.api_controller.get_matchlist(
                puuid=self.puuid,
                params=params,
            )

            if matchlist_response == []:
                break

            match_ids += matchlist_response

        return match_ids

    def _create_participant_data(self, participant, match_id):
        return ParticipantData(
            puuid=participant["puuid"],
            name=participant["summonerName"],
            champion_name=participant["championName"],
            team_id=participant["teamId"],
            match=match_id,
        )

    def _create_match_data(self, match_data_response) -> MatchData:

        return MatchData(
            id=match_data_response["metadata"]["matchId"],
            game_start=match_data_response["info"]["gameStartTimestamp"],
            game_end=match_data_response["info"]["gameEndTimestamp"],
            game_duration=match_data_response["info"]["gameDuration"],
            game_mode=match_data_response["info"]["gameMode"],
            game_type=match_data_response["info"]["gameType"],

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

        match_data.kda = calculate_kda(
            kills=participant["kills"],
            deaths=participant["deaths"],
            assists=participant["assists"],
        )

        match_data.minion_kills = participant["totalMinionsKilled"] + \
            participant["neutralMinionsKilled"]

        match_data.vision_score = participant["visionScore"]
        match_data.team_position = participant["teamPosition"]
        match_data.team_id = participant["teamId"]
        match_data.item_purchase = [
            participant[f"item{i}"] for i in range(settings.ITEM_SLOTS)]
        match_data.summoner_spells = [
            participant[f"summoner{i}Id"] for i in range(1, settings.NUMBER_OF_SUMMONER_SPELLS + 1)]

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
                self._fill_match_data(
                    match_data=match_data, participant=participant)

            participant_data = self._create_participant_data(
                participant=participant, match_id=match_data.id)

            filtered_participant_data.append(participant_data)

        return match_data, filtered_participant_data
