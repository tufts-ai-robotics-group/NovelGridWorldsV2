from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State


class SelectItem(Action):
    def __init__(self, state: State, dynamics=None, target_type=None):
        self.state = state
        self.target_type = target_type
        self.dynamics = dynamics

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        return self.target_type in agent_entity.inventory

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
    ):
        if not self.check_precondition(agent_entity, self.target_type, target_object):
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot select item of type {self.target_type}.'
            )
        agent_entity.selectedItem = self.target_type
