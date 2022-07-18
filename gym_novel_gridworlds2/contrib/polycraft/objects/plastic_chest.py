from .polycraft_obj import PolycraftObject


class PlasticChest(PolycraftObject):
    def __init__(self, typee, loc=(0, 0), state="block", inventory=None, **kwargs):
        self.type = typee
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating

    def placement_reqs(self, map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            pass  # unbreakable object
        if action_name == "collect":
            if "blue_key" in agent.inventory:
                agent.inventory["blue_key"] += 1
            else:
                agent.inventory.update({"blue_key": 1})
