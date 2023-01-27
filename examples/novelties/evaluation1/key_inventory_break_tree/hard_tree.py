from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftEntity, PolycraftObject
from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

class HardTree(PolycraftObject):
    breakable = False
    breakable_holding = []
    
    def acted_upon(self, action_name, agent: PolycraftEntity):
        if action_name == "break":
            if "blue_key" not in agent.inventory or agent.inventory["blue_key"] == 0:
                raise PreconditionNotMetError("Show me your blue key to break me.")
            else:
                self.state = "floating"
        super().acted_upon(action_name, agent)
