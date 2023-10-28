import requests

from home_assistant_control.utils.api import make_request


def get_entities(client, category):
    return client.entities.categories[category]


class Payload:
    """
    A generic class for creating payloads for Home Assistant RESTful API calls.

    Usage example:
    >>> payload = Payload('switch.fan')
    >>> print(payload.get_payload())
    {'entity_id': 'switch.fan'}
    """

    def __init__(self, entity_name: str):
        """
        Initializes a new instance of the Payload class.

        Args:
            entity_name (str): The name of the entity.
        """
        self.entity_name = entity_name

    def get_payload(self) -> dict:
        """
        Generates the payload dictionary.

        Returns:
            dict: The payload dictionary.
        """
        return {'entity_id': self.entity_name}

    @property
    def payload(self):
        return self.__payload


class Controller:
    """
    A generic controller class for interacting with Home Assistant entities.

    Usage example:
    >>> controller = Controller(client, 'switches')
    """
    API_STUB = '/api/'
    STATE_ENDPOINT = f'{API_STUB}states/'

    def __init__(self, entity):
        """
        Initializes a new instance of the Controller class.

        Args:
            client: The Home Assistant client object.
            category_name (str): The category of the entity (e.g., 'lights', 'switches').
        """
        self.__client = entity.client
        self.__entity = entity
        self.__last_response = None
        self.category_name = self.entity.category

    @property
    def category_name(self):
        return self.__category_name

    @category_name.setter
    def category_name(self, new):
        """
        Set the value of the category_name attribute.

        Parameters:
            new (str): The new category name to be set.

        Raises:
            ValueError: If the new category name is not a string or not one of the valid categories.

        Returns:
            None
        """
        # Make sure category_name is a string
        if not isinstance(new, str):
            raise ValueError('Invalid category name! Category name must be a string!')

        # Make sure category_name is one of the valid categories
        if new not in self.client.entity_category_names:
            raise ValueError(f'Invalid category name: {new}. Must be one of {self.client.entity_category_names}')

        # Set the category_name
        self.__category_name = new

    @property
    def client(self):
        return self.__client

    @property
    def entity(self):
        return self.__entity

    @property
    def last_response(self):
        return self.__last_response

    def get_entity_state(self):
        """
        Get the state of the entity.
        """
        return make_request(
                f'{self.client.url}{self.STATE_ENDPOINT}{self.entity.entity_id}',
                self.client.token
                ).json()

    def send_payload(self, payload: dict):
        """
        Sends a payload to the Home Assistant server.

        Args:
            payload (dict): The payload to send.

        Returns:
            None: The method is responsible for sending the payload to the server.
        """
        # Logic to send the payload to the Home Assistant server goes here
        # For instance, using your `self.__client` object
        payload =

    def _post(self, url, data, headers):

        res = requests.post(url, headers=headers, json=data)

        if res.status_code != 200:
            res.raise_for_status()

        self.__last_response = res
