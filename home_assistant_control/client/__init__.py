from home_assistant_control.entities import EntityJSON, Entity, Entities
from home_assistant_control.utils import validate_and_transform_url
from home_assistant_control.utils.api import validate_and_return_token, validate_token


class Client:

    def __init__(self, url, token):
        self.__url = validate_and_transform_url(url)
        self.__token = validate_and_return_token(self.__url, token)

        self.entity_json = EntityJSON(self.__url, self.__token)
        self.entities = Entities(self, self.entity_json)

        self.entity_data = None
        self.entities.refresh()

    @property
    def entity_category_names(self):
        return sorted(list(self.entities.categories.keys()))

    def refresh(self):
        self.entities.refresh()
        self.entity_data = self.entities.entity_json

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new):
        try:
            self.__url = validate_and_transform_url(new)
        except ValueError as e:
            raise e from e

        self.refresh()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, new):
        try:
            if not validate_token(self.url, new):
                raise ValueError('Invalid token!')
        except Exception as e:
            raise ValueError(f'Invalid token: {e}') from e

        self.__token = new
