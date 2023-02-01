from gym_novel_gridworlds2.actions.action import PreconditionNotMetError
from gym_novel_gridworlds2.contrib.polycraft.actions import Trade

class KeyTrade(Trade):
    def do_action(self, agent_entity, target_type=None, target_object=None, **kwargs):
        if "blue_key" not in agent_entity.inventory or agent_entity.inventory["blue_key"] == 0:
            raise PreconditionNotMetError("Show me your blue key to trade with me.")
        return super().do_action(agent_entity, target_type, target_object, **kwargs)
