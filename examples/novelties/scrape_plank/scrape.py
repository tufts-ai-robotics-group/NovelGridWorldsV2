from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class Scrape(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the scrape action:
        1) The agent is facing an object
        2) The object is scrapeable
        """
        # convert the entity facing direction to coords
        direction = (0, 0)
        if agent_entity.facing == "NORTH":
            direction = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            direction = (1, 0)
        elif agent_entity.facing == "EAST":
            direction = (0, 1)
        else:
            direction = (0, -1)

        correctDirection = False

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1:
            correctDirection = True
            unbreakableObjects = ["bedrock", "plastic_chest", "safe"]
            if objs[0][0].type in unbreakableObjects:
                return False

        return correctDirection and (objs[0][0].state == "block")

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then scrapes the object
        """
        if not self.check_precondition(agent_entity, target_object):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot perform scrape on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("scrape", agent_entity)