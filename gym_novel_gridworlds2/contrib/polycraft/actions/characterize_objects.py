from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class CharacterizeObjects(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_additional_action = True

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the NOP action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, target_object: Object = None, **kwargs):
        """
        Checks for precondition, then does nothing
        """
        self.result = "SUCCESS"
        return {}
