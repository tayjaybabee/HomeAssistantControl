from home_assistant_control.controllers import Controller, Payload
from home_assistant_control.controllers.lights.maps import COLORS
from home_assistant_control.utils import get_headers

from home_assistant_control.controllers import LOGGER as LOG_DEVICE

# OopCompanion:suppressRename


LOGGER = LOG_DEVICE.get_child('lights')


class LightPayload(Payload):
    """
    A subclass of Payload for creating light-specific payloads.

    Usage example:
    >>> payload = LightPayload('living_room')
    >>> print(payload.get_payload())
    {'entity_id': 'light.living_room'}
    """

    ENDPOINT = 'services'

    def __init__(self, entity_name: str):
        """
        Initializes a new instance of the LightPayload class.

        Args:
            entity_name (str): The name of the entity.
        """
        super().__init__(f'light.{entity_name}')

    def set_color(self, color_name: str):
        """
        Sets the color of the light.

        Args:
            color_name (str): The name of the color.

        Usage example:
        >>> payload = LightPayload('living_room')
        >>> payload.set_color('blue')
        """
        log = self.log_device.logger
        log.debug(f'Setting color: {color_name}')
        color_name = color_name.lower()
        if color_name in COLORS:
            self.payload['rgb_color'] = COLORS[color_name]
        else:
            raise ValueError(f"Unknown color: {color_name}")

        log.debug(f'Payload is now: {self.payload}')

    def set_brightness(self, brightness: int):
        """
        Sets the brightness of the light.

        Args:
            brightness (int): The brightness level (0-255).

        Usage example:
        >>> payload = LightPayload('living_room')
        >>> payload.set_brightness(128)
        """
        log = self.log_device.logger
        log.debug(f'Setting brightness: {brightness}')
        if 0 <= brightness <= 255:
            self.payload['brightness'] = brightness
        else:
            raise ValueError("Brightness must be between 0 and 255")

        log.debug(f'Payload is now: {self.payload}')


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
    TOGGLE_ENDPOINT = f'{SERVICES_STUB}toggle'

    SERVICE_URL_MAP = {
            'turn_on':    ON_ENDPOINT,
            'turn_off':   OFF_ENDPOINT,
            'toggle':     TOGGLE_ENDPOINT,
            'brightness': ON_ENDPOINT,
            }

    def __init__(self, entity, **kwargs):
        """
        Initializes a new instance of the LightController class.

        Args:
            entity (Entity): The entity to control.
        """
        super().__init__(entity, **kwargs)

    @property
    def service_payload(self):
        """
        Returns the payload for the light service.

        Returns:
            LightPayload: The payload object for the light service.

        Args:
            self: The instance of the LightController class.
        """
        return LightPayload(self.entity.name)

    def change_attributes(self, **kwargs):
        """
        Changes the attributes of the light.

        Returns:
            None

        Args:
            self: The instance of the LightController class.
        """
        payload = self.service_payload
        log = self.log_device.logger

        log.debug(f'Received kwargs: {kwargs}')

        # Set color if provided.
        if 'color' in kwargs:
            payload.set_color(kwargs['color'])

        # Set brightness if provided.
        if 'brightness' in kwargs:
            payload.set_brightness(kwargs['brightness'])

        return self.call_service('turn_on', payload=payload.payload)

    def get_state(self):
        """
        Returns the state of the light.

        Returns:
            str: The state of the light.

        Args:
            self: The instance of the LightController class.
        """
        return self.get_entity_state()['state']

    def _post(self, url, data):
        """
        Overrides the _post method in the Controller class.

        Returns:
            None

        Args:
            self: The instance of the LightController class.
        """
        log = self.log_device.logger
        headers = get_headers(self.client.token)

        log.debug(f'Sending headers: {headers}')

        return super()._post(url, headers=headers, data=data)

    def get_endpoint_url(self, service):
        """
        Returns the endpoint URL for the light service.

        Returns:
            str: The endpoint URL for the light service.

        Args:
            self: The instance of the LightController class.
        """
        ep = self.SERVICE_URL_MAP.get(service.lower())
        print(ep)
        return f'{self.client.url}{ep}'

    def turn_on(self):
        """
        Turns the light on.

        Returns:
            None

        Args:
            self: The instance of the LightController class.
        """
        return self.call_service('turn_on')

    def turn_off(self):
        return self.call_service('turn_off')

    def toggle(self):
        """
        Toggles the state of the light.

        Returns:
            None

        Args:
            self: The instance of the LightController class.
        """
        return self.call_service('toggle')

    def call_service(self, service_name, payload=None):

        url = self.get_endpoint_url(service_name.lower())
        print(url)
        data = payload or self.service_payload.payload
        print(data)

        return self._post(url, data)
