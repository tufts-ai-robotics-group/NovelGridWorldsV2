from .unbreakable_polycraft_obj import UnbreakablePolycraftObject
from gym_novel_gridworlds2.utils.inventory_utils import merge_inventory


class Safe(UnbreakablePolycraftObject):
    def __init__(self, type="safe", loc=(0, 0), state="block", inventory=None, **kwargs):
        super().__init__(**kwargs)
        if inventory is None:
            inventory = {"diamond": 18}
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.isLocked = True
        self.inventory = inventory

    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            pass  # unbreakable
        elif action_name == "use":
            if "blue_key" in agent.inventory:
                self.isLocked = False
                self.type == "unlocked_safe"
        elif action_name == "collect" and not self.isLocked:
            merge_inventory(agent.inventory, self.inventory)
            self.inventory = {}
