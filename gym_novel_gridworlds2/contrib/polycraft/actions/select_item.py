from gym_novel_gridworlds2.actions import Action
from gym_novel_gridworlds2.object import Entity, Object

class SelectItem(Action):
    def check_precondition(self, agent_entity: Entity, target_type: str = None, target_object: Object = None, **kwargs):
        return target_type in agent_entity.inventory
    
    def do_action(self, agent_entity: Entity, target_type: str = None, target_object: Object = None):
        if self.check_precondition(agent_entity, target_type, target_object):
            pass
