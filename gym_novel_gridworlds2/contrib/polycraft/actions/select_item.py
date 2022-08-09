from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion, backConversion


class SelectItem(Action):
    def __init__(self, target_type, **kwargs):
        self.target_type = backConversion(target_type)
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
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity, self.target_type, target_object):
            self.result = "FAILED"
            self.action_metadata(agent_entity, target_type, target_object)
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot select item of type {self.target_type}.'
            )
        agent_entity.selectedItem = self.target_type

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity, target_type, target_object)

    def action_metadata(
        self, agent_entity, target_type=None, target_object=None, **kwargs
    ):
        return "".join(
            "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: '"
            + str(self.state.goalAchieved)
            + ", “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “select_item”, “argument”: “"
            + nameConversion(self.target_type)
            + "”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 120}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
