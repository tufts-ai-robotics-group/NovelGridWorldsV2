from typing import Optional
from ..object.entity import Entity, Object
from ..state.state import State


class PreconditionNotMetError(Exception):
    def __init__(self, message=""):
        self.message = message
    pass


class Action:
    def __init__(self, state: State, dynamics=None, cmd_format=None, **kwargs):
        """
        Initialize action with a reference to the state, the dynamics, and respective actions.
        """
        self.dynamics = dynamics
        self.state = state
        if cmd_format is not None:
            self.cmd_format = cmd_format

        # sets if the agent can do an additional action
        self.allow_additional_action = False
        pass

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs
    ):
        """
        Given the agent and the target
        (either type of object or a reference to a specific object)
        plus corresponding extra arguments,
        returns if the action's precondition is met.
        """
        pass

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
    ):
        """
        Given the agent and the target
        (either type of object or a reference to a specific object)
        plus corresponding extra arguments,
        Do the action if the action's precondition is met.
        Raises error if the action's precondition is not met.
        """
        pass

    def action_metadata(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
    ):
        """
        Prints out the metadata of the action after execution, i.e:
        {“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”},
        “command_result”: {“command”: “break_block”, “argument”: “”,
        “result”: “SUCCESS”, “message”: “”, “stepCost: 3600},
        “step”:7, “gameOver”:false}
        """
        pass
