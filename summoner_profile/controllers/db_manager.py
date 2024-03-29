from django.core.exceptions import ObjectDoesNotExist

from summoner_profile.models import (
    ChampionStats,
    Item,
    Participant,
    RankedStats,
    Match,
    Summoner,
    SummonerSpell,

)
from summoner_profile.utils.utils import calculate_kda

from summoner_profile.utils.dataclasses import (
    ParticipantData,
    RankedStatsData,
    SummonerData,
    MatchData,
    ResponseData,
    ChampionStatsData,
    ItemData,
    SummonerSpellData,
)


class DbManager:

    def __init__(self, puuid: str = None) -> None:
        self._summoner_instance = None
        self._puuid = puuid

    @property
    def summoner_instance(self):
        return self._summoner_instance

    @summoner_instance.setter
    def summoner_instance(self, new_value: Summoner):
        if isinstance(new_value, Summoner):
            self._summoner_instance = new_value

    @property
    def puuid(self):
        return self._puuid

    def is_puuid_in_database(self) -> bool:
        """Comprueba si el puuid del Summoner esta en la base de dato
        """

        return Summoner.objects.filter(puuid=self.puuid).exists()

    def last_update(self) -> int:
        """Devuelve el timestamp de la ultima actualizacion de los datos del Summoner.
        """

        try:
            last_update = Summoner.objects.get(puuid=self.puuid).last_update

            return int(last_update)

        except ObjectDoesNotExist:
            return False

    # Metodos Update
    def update_summoner(self, data: SummonerData) -> None:
        """Actualiza los datos del Summoner en la base de datos.
        """

        defaults = {
            "id": data.id,
            "name": data.name,
            "icon_id": data.icon_id,
            "summoner_level": data.summoner_level,
            "last_update": data.last_update,
        }

        Summoner.objects.update_or_create(puuid=data.puuid, defaults=defaults)

        # Obtengo la instancia del summoner que acabo de actualizar para poder usarla en los siguientes metodos
        self.summoner_instance = Summoner.objects.get(puuid=self.puuid)

    def update_ranked_stats(self, data: list[RankedStatsData]) -> None:
        """Actualiza los datos de RankedStats en la base de datos.
        """

        for ranked_stats in data:
            defaults = {
                "tier": ranked_stats.tier,
                "rank": ranked_stats.rank,
                "league_points": ranked_stats.league_points,
                "wins": ranked_stats.wins,
                "losses": ranked_stats.losses,
                "winrate": ranked_stats.winrate,

            }

            RankedStats.objects.update_or_create(
                queue_type=ranked_stats.queue_type, summoner=self.summoner_instance, defaults=defaults)

    def update_match_data(self, data: list[MatchData]) -> None:
        """Actualiza los datos de Match en la base de datos.
        """

        for match_data in data:

            defaults = {
                "game_start": match_data.game_start,
                "game_end": match_data.game_end,
                "game_duration": match_data.game_duration,
                "game_mode": match_data.game_mode,
                "game_type": match_data.game_type,
                "champion_played": match_data.champion_played,
                "win": match_data.win,
                "kills": match_data.kills,
                "deaths": match_data.deaths,
                "assists": match_data.assists,
                "kda": match_data.kda,
                "minion_kills": match_data.minion_kills,
                "vision_score": match_data.vision_score,
                "team_position": match_data.team_position,
                "team_id": match_data.team_id,

                "summoner": self.summoner_instance,
            }

            match, created = Match.objects.update_or_create(
                id=match_data.id, defaults=defaults)

            # Obtiene los objetos Item para los items comprados en este match
            items = Item.objects.filter(id__in=match_data.item_purchase)

            # Agrega los items al match
            match.item_purchase.set(items)

            # Obtiene los objetos Participant para los participantes de este match
            summoner_spells = SummonerSpell.objects.filter(
                key__in=match_data.summoner_spells)

            #  Agrego los summoner spells al match
            match.summoner_spells.set(summoner_spells)

    def update_participants_data(self, data: list[ParticipantData]) -> None:
        """Actualiza los datos de Participant en la base de datos.
        """

        for participant_data in data:

            # Obtengo la instancia de Match a la que pertenece el participante
            match_instance = Match.objects.get(id=participant_data.match)

            defaults = {
                "name": participant_data.name,
                "champion_name": participant_data.champion_name,
                "team_id": participant_data.team_id,
            }

            Participant.objects.update_or_create(
                puuid=participant_data.puuid, match=match_instance, defaults=defaults)

    def update_champion_stats(self) -> None:
        """Actualiza los datos de ChampionStats en la base de datos."""

        # Obtiene los matches del summoner
        matches = Match.objects.filter(summoner=self.summoner_instance)

        for match in matches:
            # Obtiene el nombre del campeon jugado en ese match
            champion_name = match.champion_played

            # Busca una entrada existente de ChampionStats con ese nombre de campeon y summoner
            champion_stats, created = ChampionStats.objects.get_or_create(
                name=champion_name,
                summoner=self.summoner_instance,
            )

            # Actualiza las estadisticas del campeon para este match
            champion_stats.games += 1
            champion_stats.wins += 1 if match.win else 0
            champion_stats.losses += 1 if not match.win else 0
            champion_stats.kills = round(
                (champion_stats.kills * (champion_stats.games - 1) + match.kills) / champion_stats.games, 1)
            champion_stats.deaths = round(
                (champion_stats.deaths * (champion_stats.games - 1) + match.deaths) / champion_stats.games, 1)
            champion_stats.assists = round(
                (champion_stats.assists * (champion_stats.games - 1) + match.assists) / champion_stats.games, 1)
            champion_stats.kda = round(calculate_kda(
                champion_stats.kills, champion_stats.deaths, champion_stats.assists), 2)
            champion_stats.minion_kills = round((champion_stats.minion_kills * (
                champion_stats.games - 1) + match.minion_kills) / champion_stats.games, 1)
            champion_stats.winrate = int(
                (champion_stats.wins / champion_stats.games) * 100)

            champion_stats.save()

    # Periodic Update methods
    def update_items(self, items: list) -> None:
        """Actualiza los datos de Item en la base de datos.
        """

        for item in items:

            Item.objects.update_or_create(
                id=item["id"],
                defaults=item,

            )

    def update_summoner_spells(self, summoner_spells: list) -> None:
        """Actualiza los datos de SummonerSpell en la base de datos.
        """

        for spell in summoner_spells:

            SummonerSpell.objects.update_or_create(
                id=spell["id"],
                defaults=spell,
            )

    # Fetch Methods
    def _fetch_summoner_data(self) -> SummonerData:
        """Devuelve un objeto SummonerData con los datos del Summoner."""

        self.summoner_instance = Summoner.objects.get(puuid=self.puuid)

        return SummonerData(
            puuid=self.summoner_instance.puuid,
            id=self.summoner_instance.id,
            name=self.summoner_instance.name,
            icon_id=self.summoner_instance.icon_id,
            summoner_level=self.summoner_instance.summoner_level,
            last_update=self.summoner_instance.last_update,
        )

    def _fetch_ranked_stats_data_list(self) -> list[RankedStatsData]:
        """Devuelve una lista de objetos RankedStatsData con los datos de RankedStats del Summoner
        """

        ranked_stats = RankedStats.objects.filter(
            summoner=self.summoner_instance)

        ranked_stats_data_list: list[RankedStatsData] = []

        for ranked_stats_entry in ranked_stats:

            ranked_stats_data = RankedStatsData(
                queue_type=ranked_stats_entry.queue_type,
                tier=ranked_stats_entry.tier,
                rank=ranked_stats_entry.rank,
                league_points=ranked_stats_entry.league_points,
                wins=ranked_stats_entry.wins,
                losses=ranked_stats_entry.losses,
                winrate=ranked_stats_entry.winrate,
            )

            ranked_stats_data_list.append(ranked_stats_data)

        return ranked_stats_data_list

    def _fetch_champion_stats_data_list(self, champion_amount: int = 7) -> list[ChampionStatsData]:
        """Devuelve una lista de objetos ChampionStatsData con los datos de ChampionStats del Summoner
        """

        # Obtiene los champion_stats ordenados descendientemente por games jugados y toma los primeros (champion_amount) campeones
        champion_stats = ChampionStats.objects.filter(
            summoner=self.summoner_instance).order_by("-games")[:champion_amount]

        champion_stats_data_list: list[ChampionStatsData] = []

        for champion_stats_entry in champion_stats:

            champ_stats_data = ChampionStatsData(
                name=champion_stats_entry.name,
                games=champion_stats_entry.games,
                wins=champion_stats_entry.wins,
                losses=champion_stats_entry.losses,
                winrate=champion_stats_entry.winrate,
                kills=champion_stats_entry.kills,
                deaths=champion_stats_entry.deaths,
                assists=champion_stats_entry.assists,
                kda=champion_stats_entry.kda,
                minion_kills=champion_stats_entry.minion_kills,
            )
            champion_stats_data_list.append(champ_stats_data)

        return champion_stats_data_list

    def _fetch_item_purchase(self, match: Match) -> list[ItemData]:
        """Devuelve una lista de objetos ItemData con los datos de los items comprados en el match
        """

        items = match.item_purchase.all()
        item_purchase: list[ItemData] = []

        for item in items:
            item_data = ItemData(
                id=item.id,
                name=item.name,
                plaintext=item.plaintext,
                description=item.description,
                gold_base=item.gold_base,
                gold_total=item.gold_total,
            )
            item_purchase.append(item_data)

        return item_purchase

    def _fetch_summoner_spells(self, match: Match) -> list[SummonerSpellData]:
        """Devuelve una lista de objetos SummonerSpellData con los datos de los summoner spells usados por el Summoner en el match
        """

        spells = match.summoner_spells.all()
        summoner_spells: list[SummonerSpellData] = []

        for spell in spells:
            summ_spell_data = SummonerSpellData(
                id=spell.id,
                name=spell.name,
                key=spell.key,
                description=spell.description,
                image_name=spell.image_name,
                sprite_name=spell.sprite_name,
            )
            summoner_spells.append(summ_spell_data)

        return summoner_spells

    def _fetch_participants(self, match: Match) -> list[ParticipantData]:
        """Devuelve una lista de objetos ParticipantData con los datos de los participantes del match
        """

        participants_query = match.participants.all()

        participants: list[ParticipantData] = []

        for participant in participants_query:
            participant_data = ParticipantData(
                puuid=participant.puuid,
                name=participant.name,
                champion_name=participant.champion_name,
                team_id=participant.team_id,
                match=match.id,
            )
            participants.append(participant_data)

        return participants

    def _fetch_match_data_list(self, match_amount: int = 10) -> list[MatchData]:
        """Devuelve una lista de objetos MatchData con los datos de los matches del Summoner ordenados descendientemente por game_start tomando los primeros (match_amount) matches
        """

        matches = Match.objects.filter(summoner=self.summoner_instance).order_by(
            "-game_start")[:match_amount]

        match_data_list: list[MatchData] = []

        for match_ in matches:

            # Obtiene los items comprados en este match
            item_purchase = self._fetch_item_purchase(match_)

            # Obtiene los summoner spells usados en este match
            summoner_spells = self._fetch_summoner_spells(match_)

            # Obtiene los participantes de este match mediante la relacion inversa de match.participants
            participants = self._fetch_participants(match_)

            match_data = MatchData(
                id=match_.id,
                game_start=match_.game_start,
                game_end=match_.game_end,
                game_duration=match_.game_duration,
                game_mode=match_.game_mode,
                game_type=match_.game_type,
                champion_played=match_.champion_played,
                win=match_.win,
                kills=match_.kills,
                deaths=match_.deaths,
                assists=match_.assists,
                kda=match_.kda,
                minion_kills=match_.minion_kills,
                vision_score=match_.vision_score,
                team_position=match_.team_position,
                team_id=match_.team_id,
                item_purchase=item_purchase,
                summoner_spells=summoner_spells,
                participants=participants,
            )
            match_data_list.append(match_data)

        return match_data_list

    def fetch_response_data(self) -> ResponseData:
        """Devuelve un objeto ResponseData con los datos requeridos para la respuesta de la API
        """

        return ResponseData(
            summoner_data=self._fetch_summoner_data(),
            ranked_stats_data_list=self._fetch_ranked_stats_data_list(),
            champion_stats_data_list=self._fetch_champion_stats_data_list(),
            match_data_list=self._fetch_match_data_list(),
        )
