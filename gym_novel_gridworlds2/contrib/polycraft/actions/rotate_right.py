from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class RotateRight(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the rotate_right action:
        1) None! You can always rotate
        """
        return True

    def do_action(self, agent_entity, target_type=None, target_object=None):
        """
        Rotates the object to the right
        """
        if agent_entity.facing == "NORTH":
            agent_entity.facing = "EAST"
        elif agent_entity.facing == "EAST":
            agent_entity.facing = "SOUTH"
        elif agent_entity.facing == "SOUTH":
            agent_entity.facing = "WEST"
        else:
            agent_entity.facing = "NORTH"

        self.result = "SUCCESS"
        self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        print(
            "{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “smooth_turn”, “argument”: “90”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 24}, “step”:1, “gameOver”:false}"
        )
