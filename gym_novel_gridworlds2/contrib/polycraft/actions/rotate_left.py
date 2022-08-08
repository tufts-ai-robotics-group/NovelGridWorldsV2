from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class RotateLeft(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the rotate_left action:
        1) None! You can always rotate
        """
        return True

    def do_action(self, agent_entity, target_type=None, target_object=None, **kwargs):
        """
        Rotates the object to the left
        """
        # self.state._step_count += 1
        self.state.incrementer()
        if agent_entity.facing == "NORTH":
            agent_entity.facing = "WEST"
        elif agent_entity.facing == "EAST":
            agent_entity.facing = "NORTH"
        elif agent_entity.facing == "SOUTH":
            agent_entity.facing = "EAST"
        else:
            agent_entity.facing = "SOUTH"

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        return "".join(
            "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: '"
            + str(self.state.goalAchieved)
            + ", “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “smooth_turn”, “argument”: “-90”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 24}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
