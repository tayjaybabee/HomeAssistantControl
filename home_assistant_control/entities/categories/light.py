from home_assistant_control.entities.categories import Category
from home_assistant_control.controllers.lights import LightController


# OopCompanion:suppressRename


class LightCategory(Category):
    def __init__(self, client, category_name):
        super().__init__(client, 'light')

    def _gather_members(self):
        members = super()._gather_members()
        print(members)
        for member in members:
            member.controller = LightController(member)

        return members

    def turn_all_off(self):
        """
        Turns all lights off.

        Returns:
            None

        """
        for member in self.members:
            member.controller.turn_off()

    def turn_all_on(self):
        """
        Turn on all lights.

        Returns:
            None
        """
        for member in self.members:
            member.controller.turn_on()

    def toggle_all(self):
        """
        Toggles the state of all lights.

        Returns:
            None

        """
        for member in self.members:
            member.controller.toggle()

    def change_attributes_of_all(self, **kwargs):
        """
        Changes the attributes of all lights.

        Returns:
            None

        """
        for member in self.members:
            member.controller.change_attributes(**kwargs)
