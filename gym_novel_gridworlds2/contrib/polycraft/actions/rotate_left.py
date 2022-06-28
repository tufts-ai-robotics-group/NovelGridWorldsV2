from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class RotateLeft(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the rotate_left action:
        1) None! You can always rotate
        """
        return True

    def do_action(self, agent_entity, target_type=None, target_object=None):
        """
        Rotates the object to the left
        """
        if agent_entity.facing == "NORTH":
            agent_entity.facing = "WEST"
        elif agent_entity.facing == "EAST":
            agent_entity.facing = "NORTH"
        elif agent_entity.facing == "SOUTH":
            agent_entity.facing = "EAST"
        else:
            agent_entity.facing = "SOUTH"
