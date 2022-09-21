from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject


class Hole(PolycraftObject):
    def __init__(self, type, loc=(0, 0), state="block", inventory=None, **kwargs):
        if inventory is None:
            inventory = {}
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.canWalkOver = True
        self.inventory = inventory

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        """if action_name == "use":
            if self.canWalkOver == True:
                self.canWalkOver = False
            else:
                self.canWalkOver = True"""
        if action_name == "break":
            agent.inventory.update(self.inventory)
            self.state = "floating"