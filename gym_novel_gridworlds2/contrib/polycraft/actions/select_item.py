from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State


class SelectItem(Action):
    def __init__(self, state: State, dynamics=None, **kwargs):
        self.state = state
        self.dynamics = dynamics

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        return target_type in agent_entity.inventory

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
    ):
        if not self.check_precondition(agent_entity, target_type, target_object):
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot select item of type {target_type}.'
            )
        agent_entity.selectedItem = target_type
