from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion, backConversion


class SelectItem(Action):
    def __init__(self, target_type=None, **kwargs):
        self.target_type = target_type
        self.cmd_format = r"[^\s]+ (?P<target_type>[^\s]+)"
        super().__init__(**kwargs)

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        return target_type in agent_entity.inventory or target_type is None

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        if target_type is None and self.target_type is None:
            # if the params is empty, it is the deselect action
            agent_entity.selectedItem = None
            return {}
        elif target_type is None:
            target_type = backConversion(self.target_type)
        else:
            target_type = backConversion(target_type)
        self.state.incrementer()

        if not self.check_precondition(agent_entity, target_type, target_object):
            self.result = "FAILED"
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot select item of type {target_type}.'
            )
        agent_entity.selectedItem = target_type

        return {}
