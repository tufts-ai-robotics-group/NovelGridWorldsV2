from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject


class CraftingTable(PolycraftObject):
    def __init__(self, type, loc=(0, 0), state="block", fire_state="on_fire", **kwargs):
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: on_fire and available
        self.fire_state = fire_state
        self.canWalkOver = False

    def placement_reqs(self, map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "spray_water" and agent.inventory["water"] > 0:
            self.fire_state = "available"
            agent.inventory["water"] -= 1
        if action_name == "break":
            self.state = "floating"