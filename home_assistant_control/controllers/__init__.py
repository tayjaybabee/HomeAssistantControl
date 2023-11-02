import requests
from time import sleep
from home_assistant_control.utils.api import make_request


from home_assistant_control.log_engine import LOG_DEVICE, Loggable


LOGGER = LOG_DEVICE.get_child('controllers')


def get_entities(client, category):
    return client.entities.categories[category]


class Payload(Loggable):
    """
    A generic class for creating payloads for Home Assistant RESTful API calls.

    Usage example:
    >>> payload = Payload('switch.fan')
    >>> print(payload.get_payload())
    {'entity_id': 'switch.fan'}
    """

    def __init__(self, entity_id, parent_log_device=LOGGER):
        """
        Initializes a new instance of the Payload class.

        """
        super().__init__(parent_log_device=parent_log_device)
        self.__entity_id = entity_id
        self.__payload = {
            'entity_id': entity_id,
        }

        log = self.log_device.logger

        log.debug(f'Entity ID: {self.entity_id}')

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def entity_name(self):
        return '.'.join(self.entity_id.split('.')[1:])

    def get_payload(self) -> dict:
        """
        Generates the payload dictionary.

        Returns:
            dict: The payload dictionary.
        """
        return self.payload

    @property
    def payload(self):
        return self.__payload


class Controller(Loggable):
    """
    A generic controller class for interacting with Home Assistant entities.

    Usage example:
    >>> controller = Controller(client, 'switches')
    """
    API_STUB = '/api/'
    STATE_ENDPOINT = f'{API_STUB}states/'

    def __init__(
            self,
            entity,
            return_status=True,
            parent_log_device=LOGGER
    ):
        """
        Initializes a new instance of the Controller class.

        Args:
            entity (Entity):
                The entity to control.

            return_status (Optional, bool):
                Whether to return the entity state after sending a state-change request.(Defaults to True)
        """
        super().__init__(parent_log_device=parent_log_device)
        self.__client = entity.client
        self.__entity = entity
        self.__last_response = None
        self.__return_status = return_status

        self.category_name = self.entity.category
        self.entity_name = self.entity.name
        self.entity_id = self.entity.entity_id

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

    @property
    def return_status(self):
        return self.__return_status

    @return_status.setter
    def return_status(self, new):
        log = self.log_device.logger
        log.debug(f'Setting `return_status` to {new}')
        if not isinstance(new, bool):
            raise ValueError('return_status must be a boolean!')

        self.__return_status = new

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
        pass

    def _post(self, url, data, headers):
        log = self.log_device.logger
        log.debug(f'Sending POST request to {url} with data: {data}')
        res = requests.post(url, headers=headers, json=data)

        if res.status_code != 200:
            res.raise_for_status()

        log.debug(f'Received status code: {res.status_code}')
        log.debug(f'Received response: {res.text}')

        self.__last_response = res

        if self.return_status:
            log.debug('Checking entity state after 1 second delay')
            sleep(1)
            log.debug(f'Entity state: {self.get_entity_state()}')

            return self.get_entity_state()
