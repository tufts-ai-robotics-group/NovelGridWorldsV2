from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError


import enum
from typing import List
from gym_novel_gridworlds2.contrib.polycraft.states.polycraft_state import (
    PolycraftState,
)
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.coord_convert import internal_to_external


class SenseActorActions(Action):
    def __init__(self, state: PolycraftState, dynamics=None, **kwargs):
        super().__init__(state, dynamics, **kwargs)
        self.dynamics = dynamics
        self.state = state
        self.allow_additional_action = True
        self.cmd_format = r"sense_actor_actions"
        self.monitored_actors = kwargs['monitored_actors']

    def check_precondition(
        self, agent_entity, target_object = None, **kwargs
    ):
        """
        Checks preconditions of the SenseAll action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, mode: str = "", **kwargs):
        output_dict = []
        for key, item in self.state.state_history.items():
            if key in self.monitored_actors:
                output_dict.append(item)
        return output_dict
