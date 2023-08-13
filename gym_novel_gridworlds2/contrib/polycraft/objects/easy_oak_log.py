from gym_novel_gridworlds2.contrib.polycraft.objects import BreakablePolycraftObject
from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftEntity


class OakLog(BreakablePolycraftObject):
    def acted_upon(self, action_name, agent: PolycraftEntity):
        if action_name == "collect":
            if agent.selectedItem == "tree_tap":
                agent.add_to_inventory("rubber", 1)
        super().acted_upon(action_name, agent)
