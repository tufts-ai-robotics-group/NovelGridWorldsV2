from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object import Entity, Object
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.contrib.polycraft.objects.chest import Chest

import numpy as np

from gym_novel_gridworlds2.state.dynamic import Dynamic
from gym_novel_gridworlds2.utils.namelogic import backConversion


class PlaceItem(Action):
    def __init__(self, **kwargs):
        self.cmd_format = r"[^\s]+ (?P<target_type>[^\s]+)"
        super().__init__(**kwargs)

    def check_precondition(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs,
    ):
        if (
            target_type == None
            or target_type == "iron_pickaxe"
        ):
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

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1 or len(objs[1]) == 1:  # contains objs, not clear
            return False
        canPlace = False
        if target_type in self.dynamics.obj_types:
            self.dynamics.obj_types[target_type]
            self.state.place_object(
                target_type,
                self.dynamics.obj_types[target_type]["module"],
                properties={
                    "loc": self.temp_loc,
                    **self.dynamics.obj_types[target_type]["params"],
                },
            )
            objs = self.state.get_objects_at(self.temp_loc)
            if objs[0][0].placement_reqs(self.state, self.temp_loc):
                canPlace = True
            self.state.remove_object(objs[0][0].type, self.temp_loc)
            # find a way to get the placement requirements out

        return agent_entity.inventory[target_type] > 0 and canPlace

    def do_action(
        self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        **kwargs
    ):
        self.state.incrementer()
        if target_type is None:
            target_type = backConversion(agent_entity.selectedItem)
        else:
            target_type = backConversion(target_type)

        if not self.check_precondition(agent_entity, target_type, target_object):
            self.result = "FAILURE"
            self.action_metadata(agent_entity, target_type, target_object)
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot place item of type {target_type}.'
            )
        if target_type == "sapling":
            itemToPlace = "oak_log"
        else:
            itemToPlace = target_type
        # place object of type selectedItem on map in the direction the agent is facing
        if target_type in self.dynamics.obj_types:
            obj_info = self.dynamics.obj_types[target_type]
            self.state.place_object(
                itemToPlace,
                obj_info["module"],
                properties={"loc": self.temp_loc, **obj_info["params"]},
            )
        elif "default" in self.dynamics.obj_types:
            obj_info = self.dynamics.obj_types["default"]
            self.state.place_object(
                itemToPlace,
                obj_info["module"],
                properties={"loc": self.temp_loc, **obj_info["params"]},
            )
        else:
            self.state.place_object(
                itemToPlace,
                Entity,
                properties={"loc": self.temp_loc},
            )
        agent_entity.inventory[target_type] -= 1

        self.result = "SUCCESS"
        return {}
