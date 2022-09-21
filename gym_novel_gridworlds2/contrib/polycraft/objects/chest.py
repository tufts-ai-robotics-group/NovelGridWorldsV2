from .polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.utils.inventory_utils import merge_inventory


class Chest(PolycraftObject):
    def __init__(self, type="chest", loc=(0, 0), state="block", inventory=None, **kwargs):
        super().__init__(**kwargs)
        if inventory is None:
            inventory = {}
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.inventory = inventory

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            merge_inventory(agent.inventory, self.inventory)
            self.state = "floating"
        if action_name == "use":
            merge_inventory(agent.inventory, self.inventory)
            self.inventory = {}
