from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftEntity, PolycraftObject

class HardTree(PolycraftObject):
    def acted_upon(self, action_name, agent: PolycraftEntity):
        if action_name == "break":
            if agent.selectedItem == "axe":
                self.state = "floating" # tree can only be broken with axe selected
            return
        super().acted_upon(action_name, agent)

