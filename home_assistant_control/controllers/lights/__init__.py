from home_assistant_control.controllers import Controller, Payload
from home_assistant_control.controllers.lights.maps import COLORS
from home_assistant_control.utils.api import make_request
from home_assistant_control.utils import get_headers


class LightPayload(Payload):
    """
    A subclass of Payload for creating light-specific payloads.

    Usage example:
    >>> payload = LightPayload('light.living_room', 'red', 255)
    >>> print(payload.get_payload())
    {'entity_id': 'light.living_room', 'rgb_color': [255, 0, 0], 'brightness': 255}
    """

    ENDPOINT = 'services'

    def __init__(self, entity_name: str):
        """
        Initializes a new instance of the LightPayload class.

        Args:
            entity_name (str): The name of the entity.
            color (str): The color to set.
            brightness (int): The brightness level.
        """
        self.__entity_name = entity_name.lower()
        self.__entity_id = f'light.{self.entity_name}'
        super().__init__(self.entity_id)

    @property
    def entity_name(self):
        return self.__entity_name

    @property
    def entity_id(self):
        return self.__entity_id

    def get_payload(self) -> dict:
        """
        Generates the payload dictionary specific to lights.

        Returns:
            dict: The light-specific payload dictionary.
        """
        return super().get_payload()


class LightController(Controller):
    """
    A class for controlling lights, inheriting from the generic Controller class.

    Usage example:
    >>> light_controller = LightController(client, 'lights')
    >>> light_controller.change_light_color('light.living_room', 'red', 255)
    """
    SERVICES_STUB = f'/api/services/light/'
    ON_ENDPOINT = f'{SERVICES_STUB}turn_on'
    OFF_ENDPOINT = f'{SERVICES_STUB}turn_off'

    SERVICE_URL_MAP = {
            'turn_on':  ON_ENDPOINT,
            'turn_off': OFF_ENDPOINT
            }

    def __init__(self, entity):
        """
        Initializes a new instance of the LightController class.

        Args:
            client: The Home Assistant client object.
            category_name (str): The category of the entity (e.g., 'lights').
        """
        super().__init__(entity)

    @property
    def service_payload(self):
        return LightPayload(self.entity.name)

    def change_light_color(self, entity_name: str, color: str, brightness=255):
        """
        Changes the color of a light entity.

        Args:
            entity_name (str): The name of the entity.
            color (str): The color to set.
            brightness (int): The brightness level.

        Returns:
            None: Sends the payload using the send_payload method from Controller.
        """
        print(entity_name)
        payload_obj = LightPayload(f'light.{entity_name}')
        payload = payload_obj.get_payload()

        # Use the send_payload method from the parent Controller class
        self.send_payload(payload)

    def get_state(self):
        return self.get_entity_state()['state']

    def _post(self, url, *args):
        headers = get_headers(self.client.token)

        return super()._post(url, headers=headers, json=data)

    def get_endpoint_url(self, service):
        ep = self.SERVICE_URL_MAP.get(service.lower())
        return f'{self.client.url}{ep}'

    def turn_on(self):
        # Assemble the url
        url = self.get_endpoint_url('turn_on')

        # Assemble the data
        data = self.service_payload

        # Post the data
        return self._post(url, data.get_payload())

    def turn_off(self):
        # Assemble the url
        url = self.get_endpoint_url('turn_off')

        data = LightPayload(self.entity.name)

        return self._post(url, data.get_payload())
