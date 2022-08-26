from .polycraft_obj import PolycraftObject


def merge_inventory(old_item, new_item):
    """
    Merges two items into one item.
    """
    for key, value in new_item.items():
        if key in old_item:
            old_item[key] += value
        else:
            old_item[key] = value


class Safe(PolycraftObject):
    def __init__(self, typee, loc=(0, 0), state="block", inventory=None, **kwargs):
        if inventory is None:
            inventory = {"diamond": 18}
        self.type = typee
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.isLocked = True
        self.inventory = inventory

    def placement_reqs(self, map_state, loc):
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
