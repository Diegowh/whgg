from sys import version
import requests


from .items_manager import ItemsManager
from .summoner_spells_manager import SummonerSpellsManager
from ..models.version import Version

from ..controllers.db_manager import DbManager


class Updater:
    '''
    Manages the updates on the json files based on the new versions of league of legends.
    '''

    # Json data urls
    VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

    def __init__(self) -> None:

        self.db_manager = DbManager()

        self._previous_version = None
        self._latest_version = None

    # Getters

    @property
    def previous_version(self):
        return self._previous_version

    @property
    def latest_version(self):
        return self._latest_version

    # Setters
    @previous_version.setter
    def previous_version(self, version: str):
        self._previous_version = version

    @latest_version.setter
    def latest_version(self, version: str):
        self._latest_version = version

    # Methods
    def update(self):

        # Setear la version previa
        version_query = Version.objects.first()
        if version_query:
            self.previous_version = version_query.version

        # Obtenemos la ultima version
        self.check_for_updates()

        if not self.is_updated():
            self._save_latest_version()
            print("No hay actualizaciones disponibles")
            return None

        # Actualizamos los items
        items_manager = ItemsManager()
        items = items_manager.fetch()
        self.db_manager.update_items(items)

        # Actualizamos los Summoner Spells
        summ_spell_manager = SummonerSpellsManager()
        summ_spells = summ_spell_manager.fetch()
        self.db_manager.update_summoner_spells(summ_spells)

    def check_for_updates(self):

        try:
            response = requests.get(self.VERSIONS_URL)
            versions_json = response.json()

        except Exception as e:
            print(e)
            return None

        if isinstance(versions_json, list) and len(versions_json) > 0:
            self.latest_version = versions_json[0]

        else:
            print("An error ocurred trying to validate versions_json type or length")
            return None

    def is_updated(self) -> bool:
        '''
        Returns True if the latest version is different to the previous one.
        '''
        return self.latest_version != self.previous_version if self.latest_version and self.previous_version else False

    def _save_latest_version(self):
        '''
        Saves self.latest_version into the database.
        '''
        version_obj, created = Version.objects.get_or_create(
            version=self.latest_version,
            defaults={
                'version': self.latest_version,
            }
        )
        if not created:
            version_obj.version = self.latest_version
            version_obj.save()

    def force_update(self):
        '''
        Forces the update of the database.
        '''

        # Actualizamos los items
        items_manager = ItemsManager()
        items = items_manager.fetch()
        self.db_manager.update_items(items)

        # Actualizamos los Summoner Spells
        summ_spell_manager = SummonerSpellsManager()
        summ_spells = summ_spell_manager.fetch()
        self.db_manager.update_summoner_spells(summ_spells)
