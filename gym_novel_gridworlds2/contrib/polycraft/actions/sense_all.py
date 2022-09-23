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

import numpy as np

########### TODO Temporary fix, to convert coordinates
FACING_DICT = {
    "NORTH": "WEST",
    "EAST": "NORTH",
    "SOUTH": "EAST",
    "EAST": "NORTH"
}

def convert_facing(original_facing):
    return FACING_DICT.get(original_facing) or "NORTH"


class SenseAll(Action):
    def __init__(self, state: PolycraftState, dynamics=None, **kwargs):
        super().__init__(state, dynamics, **kwargs)
        self.dynamics = dynamics
        self.state = state
        self.allow_additional_action = True
        self.cmd_format = r"sense_all ?(?P<mode>\w+)?"

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the SenseAll action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, mode: str = "", **kwargs):
        currRoom = 0
        for index, room in enumerate(self.state.room_coords):
            if tuple(agent_entity.loc) in room:
                currRoom = index

        if mode is not None and mode.upper() == "NONAV":
            map_dict = self.state.get_map_rep_in_range(self.state.room_coords[currRoom], nameConversion)
        else:
            map_size = self.state.get_map_size()
            map_dict = {
                "blocks": list(self.state.get_map_rep_in_type(nameConversion).reshape(-1)),
                "size": internal_to_external(map_size),
                "origin": [0, 0, 0],
            }

        return {
            "blockInFront": self.getBlockInFront(agent_entity, self.state),
            "inventory": self.getInventory(agent_entity),
            "player": {
                "pos": internal_to_external(agent_entity.loc),
                "facing": agent_entity.facing, #TODO generalize
                "yaw": 90.0,  # dummy
                "pitch": 0.0,  # dummy
            },
            "destinationPos": [0, 0, 0],
            "entities": self.getEntities(self.state, currRoom, [agent_entity]),
            "map": map_dict,
        }

    def getBlockInFront(self, agent_entity, state: PolycraftState):
        if agent_entity.facing == "NORTH":
            vec = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            vec = (1, 0)
        elif agent_entity.facing == "WEST":
            vec = (0, -1)
        else:
            vec = (0, 1)
        locInFront = tuple(np.add(agent_entity.loc, vec))
        objs = state.get_objects_at(locInFront)
        if len(objs[0]) > 0:
            obj: Object = objs[0][0]
            name, properties = nameConversion(obj.type, obj=obj)
            blockInFront = {
                "name": name,
                # TODO generalize; also see polycraft_state
                **properties
            }
        else:
            blockInFront = {"name": "minecraft:air"}
        return blockInFront

    def getInventory(self, agent_entity: Entity):
        inventory = {
            str(slot_id): {
                "item": nameConversion(item_name)[0],
                "count": count,
                "damage": 0,
                "maxdamage": 0,
                **nameConversion(item_name)[1]
            }
            for slot_id, (item_name, count) in enumerate(agent_entity.inventory.items())
        }

        # todo check if correct
        if agent_entity.selectedItem is None:
            inventory["selectedItem"] = {
                "slot": 0,    # not used, dummy slot info
                "item": "minecraft:air", # TODO
                "count": 0,
                "damage": 0,
                "maxdamage": 0,
            }
        else:
            selected_item_name, selected_item_properties = nameConversion(agent_entity.selectedItem)
            selected_item_count = agent_entity.inventory[agent_entity.selectedItem]

            inventory["selectedItem"] = {
                "slot": 0,  # not used, dummy slot info
                "item": selected_item_name,
                "count": selected_item_count,
                "damage": 0,
                "maxdamage": 0,
                **selected_item_properties
            }
        return inventory

    def getEntities(self, state: PolycraftState, room_no: int, exclude_entities=[]):
        all_entities: List[Entity] = state.get_all_entities()
        entities_dict = {}
        for obj in all_entities:
            if tuple(obj.loc) in state.room_coords[room_no] and \
                    obj not in exclude_entities: # TODO make more efficient
                entities_dict[str(obj.id)] = {
                    "type": obj.__class__.__name__,
                    "name": obj.name,
                    "id": obj.id,
                    "pos": internal_to_external(obj.loc),
                    "color": "black",
                    "equipment": [],
                }
        return entities_dict
