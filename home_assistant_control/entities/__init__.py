from abc import ABC
from collections import defaultdict
from typing import List, Dict, Any
from requests import get
from cachetools import TTLCache, cached
from datetime import datetime, timedelta, timezone
from requests import RequestException
from typing import List, Dict, Any

from home_assistant_control.utils import format_time
from home_assistant_control.utils import validate_and_transform_url
from home_assistant_control.utils.api import make_request, validate_and_return_token
from home_assistant_control.utils.cache import Publisher, Subscriber

from home_assistant_control.entities.categories import Categories, Category

from home_assistant_control.log_engine import LOG_DEVICE, Loggable


LOGGER = LOG_DEVICE.get_child('entities')


class Entity:
    """
    A base class for all entities.

    Attributes:
        entity_id (str): The ID of the entity.
        entity_data (dict): The data associated with the entity.

    Usage example:
    >>> entity = Entity('switch.living_room')
    """

    def __init__(self, entity_data: Dict[str, Any], client):
        """
        Initialize an Entity object.

        Args:
            entity_data (dict): The data associated with the entity.
        """
        self.__client = client
        self.__entity_id = entity_data['entity_id']
        self.__entity_data = entity_data
        self.__category, self.__name = self.get_category_and_name(self.__entity_id)

        self.__controller = None

    @property
    def client(self):
        return self.__client

    @property
    def controller(self):
        return self.__controller

    @controller.setter
    def controller(self, new):
        from home_assistant_control.controllers import Controller

        if not isinstance(new, Controller):
            raise TypeError('`controller` must be a Controller instance!')

        self.__controller = new

    @staticmethod
    def get_category_and_name(entity_id: str) -> list[str]:
        """
        Get the category and name of an entity.

        Args:
            entity_id (str): The ID of the entity.

        Returns:
            tuple: A tuple containing the category and name of the entity.
        """
        return entity_id.split('.')

    @property
    def entity_id(self) -> str:
        """
        Get the ID of the entity.

        Returns:
            str: The ID of the entity.
        """
        return self.__entity_id

    @property
    def entity_data(self) -> Dict[str, Any]:
        """
        Get the data associated with the entity.

        Returns:
            dict: The data associated with the entity.
        """
        return self.__entity_data

    @property
    def category(self) -> str:
        """
        Get the category of the entity.

        Returns:
            str: The category of the entity.
        """
        return self.__category

    @property
    def name(self) -> str:
        """
        Get the name of the entity.

        Returns:
            str: The name of the entity.
        """
        return self.__name


class Entities(Subscriber, ABC):

    def __init__(self, client, entity_json, cache_timeout: int = 300):
        self.__client = client

        url = self.client.url
        token = self.client.token

        self.__url = self.validate_and_transform_url(url)

        self.__entity_json = entity_json
        self.__entity_json.subscribe(self)

        self.__all_entities = defaultdict(list)
        self.__categories = {}

    @staticmethod
    def validate_and_transform_url(url):
        return validate_and_transform_url(url)

    def gather(self):
        """
        Collects and categorizes entity data by calling the EntityJSON object.
        """
        entity_data = self.__entity_json.gather()
        self._categorize_entities(entity_data)

    def _categorize_entities(self, entity_data: List[Dict[str, Any]]):
        """
        Sorts entities into their respective categories based on their types.

        Args:
            entity_data (List[Dict[str, Any]]): The entity data to categorize.
        """
        for entity in entity_data:
            entity_id = entity['entity_id']
            category_name, name = entity_id.split('.', 1)
            entity_obj = Entity(entity, self.client)

            self.__all_entities[category_name].append(entity_obj)

            # Check if category already exists, if not create it
            if category_name not in self.__categories:
                category_obj = Category(self.__client, category_name)
                self.__categories[category_name] = {
                        'object':         category_obj,
                        'member_names':   [],
                        'member_objects': {}
                        }

            # Update the category data
            self.__categories[category_name]['member_names'].append(name)
            self.__categories[category_name]['member_objects'][name] = entity_obj

    @property
    def client(self):
        return self.__client

    @property
    def categories(self) -> Dict:
        """
        Returns the dictionary of categories.

        Returns:
            dict: The dictionary of categories.
        """
        return self.__categories

    @property
    def all_entities(self) -> Dict[str, List[Entity]]:
        """
        Returns all categorized entities.

        Returns:
            Dict[str, List[Entity]]: The categorized entities.
        """
        return self.__all_entities

    @property
    def entity_json(self):
        return self.__entity_json

    def refresh(self) -> None:
        """
        Refreshes the entity data and categorization.
        """
        self.__entity_json.refresh_cache()

    def update(self):
        """
        Update method for the Subscriber interface.
        Called when `EntityJSON`'s cache is refreshed.
        """
        self.gather()  # Gather new data based on the refreshed cache

    def get_all_in_category(self, category):
        category = category.lower()
        return self.__categories[category]['member_objects']


class EntityJSON(Publisher):
    BASE_ENDPOINT = '/api/'
    STATES_ENDPOINT = '/api/states'

    def __init__(self, url: str, token: str, cache_timeout: int = 300):
        super().__init__()
        self.__url = url
        self.__token = token
        self.__cache = TTLCache(maxsize=1, ttl=cache_timeout)
        self.__cache_age = None
        self.__cache_refresh_count = 0

    def __repr__(self):
        return f'<EntityJSON url={self.__url} cache_age={self.cache_age} cache_refresh_count={self.__cache_refresh_count}>'

    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def gather(self) -> List[Dict[str, Any]]:
        """
        Gather and cache the entities data from the Home Assistant instance.

        Returns:
            List[Dict[str, Any]]: The entities data.
        """
        try:
            # Assuming make_request is defined elsewhere or is imported
            res = make_request(f'{self.__url}{self.STATES_ENDPOINT}', self.__token)
            return res.json()
        except RequestException as e:
            raise ConnectionError(f'Failed to retrieve data: {e}') from e

    def refresh_cache(self):
        """
        Refresh the cache manually.
        """
        self.__cache.clear()  # Clear the cache to force a refresh
        self.gather()  # This will update the cache
        self._notify()  # Notify subscribers.

    @property
    def cache_age(self) -> timedelta:
        """
        Get the age of the cache.

        Returns:
            timedelta: The age of the cache.
        """
        return datetime.now(timezone.utc) - self.__cache_age if self.__cache_age else None

    @property
    def cache_age_str(self) -> str:
        """
        Get the age of the cache as a human-readable string.

        Returns:
            str: The age of the cache as a human-readable string.
        """
        age = self.cache_age
        if age is None:
            return "The cache has not been refreshed yet."

        hours, remainder = divmod(age.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return format_time(hours, minutes, seconds)  # Assuming format_time is defined elsewhere or is imported

    @property
    def cache_refresh_count(self) -> int:
        """
        Get the number of times the cache has been refreshed.

        Returns:
            int: The number of times the cache has been refreshed.
        """
        return self.__cache_refresh_count
