from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftEntity, PolycraftObject
from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

class RottingTree(PolycraftObject):

    def acted_upon(self, action_name, agent: PolycraftEntity):
        self.state = "floating"
        super().acted_upon(action_name, agent)