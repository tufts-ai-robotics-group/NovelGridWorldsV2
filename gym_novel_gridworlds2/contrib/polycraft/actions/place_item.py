from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.contrib.polycraft.objects.chest import Chest

import numpy as np

from gym_novel_gridworlds2.state.dynamic import Dynamic


class PlaceItem(Action):
    def __init__(self, state: State, dynamics: Dynamic, **kwargs):
        self.state = state
        self.dynamics = dynamics

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
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

        notOccupied = False

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 0 and len(objs[1]) == 0:  # no objs so its clear
            notOccupied = True

        return (
            agent_entity.selectedItem != None
            and agent_entity.inventory[agent_entity.selectedItem] > 0
            and notOccupied
        )

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
    ):
        if not self.check_precondition(agent_entity, target_type, target_object):
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot place item of type {agent_entity.selectedItem}.'
            )
        # place object of type selectedItem on map in the direction the agent is facing
        if agent_entity.selectedItem in self.dynamics.obj_types:
            obj_info = self.dynamics.obj_types[agent_entity.selectedItem]
            self.state.place_object(
                agent_entity.selectedItem,
                obj_info["module"],
                properties={"loc": self.temp_loc, **obj_info["params"]},
            )
        elif "default" in self.dynamics.obj_types:
            obj_info = self.dynamics.obj_types["default"]
            self.state.place_object(
                agent_entity.selectedItem,
                obj_info["module"],
                properties={"loc": self.temp_loc, **obj_info["params"]},
            )
        else:
            self.state.place_object(
                agent_entity.selectedItem,
                Entity,
                properties={"loc": self.temp_loc},
            )
        agent_entity.inventory[agent_entity.selectedItem] -= 1
