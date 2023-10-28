class Category:

    def __init__(self, client, category_name: str):
        self.__category_name = category_name.lower()
        self.__client = client

        self.__entities = client.entities

    @property
    def category_name(self) -> str:
        """
        Get the name of the category.

        Returns:
            str: The name of the category.
        """
        return self.__category_name

    @category_name.setter
    def category_name(self, new: str):
        """
        Set a new name for the category.

        Args:
            new (str): The new name for the category.
        """
        self.__category_name = new.lower()

    @property
    def name(self):
        return self.category_name

    @property
    def client(self):
        """
        Get the client associated with the category.

        Returns:
            The client associated with the category.
        """
        return self.__client

    def _gather_members(self):
        """
        Gather the members of the category.
        """
        return list(self.__entities.all_entities.get(self.__category_name, []))

    @property
    def members(self):
        """
        Get the members of the category.

        Returns:
            List[Entity]: The members of the category.
        """
        return self._gather_members()

    def find_by_name(self, name):
        """
        Find an entity in this category by its name.

        Arguments:
            name (str): The name of the desired entity.

        Returns:
            Entity: The requested entity.
        """
        for entity in self.members:
            if entity.name == name.lower():
                return entity

    def search_by_name(self, query):
        """
        Searches for entities in the list of members by their name.
        Args:
            query (str): The name to search for.
        Returns:
            list: A list of entities that match the search query.
        """
        return [entity for entity in self.members if query.lower() in entity.name]

    def __repr__(self) -> str:
        """
        Get a string representation of the Category object.

        Returns:
            str: A string representation of the Category object.
        """
        member_count = len(self._gather_members())
        return f'<Category name={self.__category_name} member_count={member_count} client={self.__client}>'

    def __str__(self) -> str:
        """
        Get a user-friendly string representation of the Category object.

        Returns:
            str: A user-friendly string representation of the Category object.
        """
        return f'Category: {self.__category_name.title()}, Members: {len(self._gather_members())}'


class Categories:

    def __init__(self, client):
        self.__client = client
        self.__contents = {}

    @property
    def client(self):
        return self.__client

    @property
    def contents(self):
        if self.__contents == {}:
            for category in self.client.entities.categories:
                self.__contents[category] = {}
                self.__contents[category]['object'] = Category(self.client, category)
                self.__contents[category]['members'] = self.__contents[category]['object']._gather_members()

        return self.__contents
