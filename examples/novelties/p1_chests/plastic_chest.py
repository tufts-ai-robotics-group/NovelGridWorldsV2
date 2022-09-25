from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject


class PlasticChest(PolycraftObject):
    def __init__(self, type, loc=(0, 0), state="block", inventory=None, **kwargs):
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.inventory = {"stick": 2, "block_of_diamond": 2, "block_of_titanium": 2, "rubber": 1, "tree_tap": 1}

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        print("I am being acted upon.")
        if action_name == "break":
            print("I am being broken. :(")
            self.state = "floating"
        """if action_name == "collect":
            if "blue_key" in agent.inventory:
                agent.inventory["blue_key"] += 1
            else:
                agent.inventory.update({"blue_key": 1})"""