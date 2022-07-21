from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class NOP(Action):
    def __init__(self, state: State, trade=None, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the NOP action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then does nothing
        """
        self.state._step_count += 1
        self.result = "SUCCESS"
        self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        print(
            "{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “NOP”, “argument”: “”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 0}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
