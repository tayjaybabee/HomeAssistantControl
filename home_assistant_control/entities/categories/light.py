from home_assistant_control.entities.categories import Category
from home_assistant_control.controllers.lights import LightController


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
        for member in self.members:
            member.controller.turn_off()
