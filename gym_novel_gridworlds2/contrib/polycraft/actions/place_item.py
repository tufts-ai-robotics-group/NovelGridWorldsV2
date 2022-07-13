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
    def __init__(self, state: State, dynamics=None, **kwargs):
        self.state = state
        self.dynamics = dynamics

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        if agent_entity.selectedItem == None:
            return False
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
        print(self.dynamics)
        canPlace = False
        if agent_entity.selectedItem in self.dynamics:
            self.dynamics[agent_entity.selectedItem]
            self.state.place_object(
                agent_entity.selectedItem,
                self.dynamics[agent_entity.selectedItem]["module"],
                properties={
                    "loc": self.temp_loc,
                    **self.dynamics[agent_entity.selectedItem]["params"],
                },
            )
            objs = self.state.get_objects_at(self.temp_loc)
            if objs[0][0].placement_reqs(self.state, self.temp_loc):
                canPlace = True
            self.state.remove_object(objs[0][0].type, self.temp_loc)
            pass  # find a way to get the placement requirements out

        return (
            agent_entity.inventory[agent_entity.selectedItem] > 0
            and notOccupied
            and canPlace
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
        if agent_entity.selectedItem in self.dynamics:
            obj_info = self.dynamics[agent_entity.selectedItem]
            self.state.place_object(
                agent_entity.selectedItem,
                obj_info["module"],
                properties={"loc": self.temp_loc, **obj_info["params"]},
            )
        elif "default" in self.dynamics:
            obj_info = self.dynamics["default"]
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
