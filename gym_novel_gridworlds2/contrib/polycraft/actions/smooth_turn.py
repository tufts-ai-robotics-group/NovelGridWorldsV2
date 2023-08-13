from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

POSSIBLE_FACING = ["NORTH", "EAST", "SOUTH", "WEST"]

class SmoothTurn(Action):
    def __init__(self, **kwargs):
        self.cmd_format = r"\w+ (?P<angle>[-\w]+)"
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the rotate_right action:
        1) None! You can always rotate
        """
        return True

    def do_action(self, agent_entity, target_type=None, target_object=None, angle=0, **kwargs):
        """
        Rotates the object to the right
        """
        # self.state._step_count += 1
        

        if angle == 0:
            return {}
        
        old_facing_index = POSSIBLE_FACING.index(agent_entity.facing)
        rotate_times = round(int(angle) / 90)
        new_facing_index = (old_facing_index + rotate_times) % 4
        agent_entity.facing = POSSIBLE_FACING[new_facing_index]

        self.result = "SUCCESS"
        return {}
