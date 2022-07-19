from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np


class Interact(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the Use action:
        1) The agent is facing an entity
        2) The entity is of a valid type
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

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[1]) != 1:
            return False

        validTypes = ["trader", "pogoist"]

        return objs[1][0].type in validTypes

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then uses the object
        """
        if not self.check_precondition(agent_entity, target_object):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot perform use on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        if objs[1][0].type == "trader":
            # get its inventory, print out trades respective to that
            for item in objs[1][0].inventory:
                print("trade_" + item)
        else:
            pass
