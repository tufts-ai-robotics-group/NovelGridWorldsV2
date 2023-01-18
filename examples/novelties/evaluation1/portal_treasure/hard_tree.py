from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftEntity, PolycraftObject
from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

class HardTree(PolycraftObject):
    breakable = False
    breakable_holding = []
    
    def acted_upon(self, action_name, agent: PolycraftEntity):
        if action_name == "break":
            raise PreconditionNotMetError("The tree cannot be broken.")
        super().acted_upon(action_name, agent)
