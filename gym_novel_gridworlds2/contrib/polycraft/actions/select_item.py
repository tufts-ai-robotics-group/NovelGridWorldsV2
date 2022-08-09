from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion, backConversion


class SelectItem(Action):
    def __init__(self, target_type, **kwargs):
        self.target_type = target_type
        self.cmd_format = r"\w+ (?P<target_type>\w+)"
        super().__init__(**kwargs)

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
        if target_type is None:
            target_type = self.target_type
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_type, target_object):
            self.result = "FAILED"
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot select item of type {target_type}.'
            )
        agent_entity.selectedItem = target_type

        return {}
