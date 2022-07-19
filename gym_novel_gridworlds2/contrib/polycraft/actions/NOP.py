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
        pass
