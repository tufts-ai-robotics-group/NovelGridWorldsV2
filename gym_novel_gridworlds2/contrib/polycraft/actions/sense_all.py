import enum
from typing import List
from gym_novel_gridworlds2.contrib.polycraft.states.polycraft_state import PolycraftState

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class SenseAll(Action):
    def __init__(self, state: PolycraftState, trade=None, dynamics=None):
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
    
    def do_action(self, agent_entity: Entity, mode: str=""):
        currRoom = 0
        for index, room in enumerate(self.state.room_coords):
            if tuple(agent_entity.loc) in room:
                currRoom = index + 1

        if mode is not None and mode.upper() == "NONAV":
            print("NONAV")
            blocks = self.state.get_map_rep_in_range(self.state.room_coords[currRoom])
        else:
            blocks = list(self.state.get_map_rep_in_type().reshape(-1))

        map_size = self.state.get_map_size()

        return {
            "blockInFront": {
                "name": self.getBlockInFront(agent_entity, self.state)
            },
            "inventory": self.getInventory(agent_entity),
            "player": {
                "pos": [agent_entity.loc[0], 17, agent_entity.loc[1]],
                "facing": agent_entity.facing,
                "yaw": 90.0,  # dummy
                "pitch": 0.0  # dummy
            },
            "destinationPos": [0, 0, 0],
            "entities": self.getEntities(self.state, currRoom),
            "map": {
                "blocks": blocks,
                "size": [map_size[0], 17, map_size[1]],
                "origin": [0, 0, 0]
            },
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
            blockInFront = state.nameConversion(objs[0][0].type)
        else:
            blockInFront = "minecraft:air"
        return blockInFront


    def getInventory(self, agent_entity: Entity):
        inventory = {
            str(slot_id): {
                "item": item_name,
                "count": count,
                "damage": 0,
                "maxdamage": 0
            } for slot_id, (item_name, count) in enumerate(agent_entity.inventory.items())
        }

        # todo check if correct
        if agent_entity.selectedItem is None:
            inventory["selectedItem"] = {
                "slot": 0,    # not used, dummy slot info
                "item": "air", # TODO
                "count": 0,
                "damage": 0,
                "maxdamage": 0
            }
        else:
            selected_item_name = agent_entity.selectedItem
            selected_item_count = agent_entity.inventory[agent_entity.selectedItem]

            inventory["selectedItem"] = {
                "slot": 0,    # not used, dummy slot info
                "item": selected_item_name,
                "count": selected_item_count,
                "damage": 0,
                "maxdamage": 0
            }
        return inventory


    def getEntities(self, state: PolycraftState, room_no: int):
        all_entities: List[Entity] = state.get_all_entities()
        entities_dict = {}
        for obj in all_entities:
            if obj.loc in state.room_coords[room_no]: # TODO make more efficient
                entities_dict[str(obj.id)] = {
                "type": obj.__class__.__name__,
                "name": obj.name,
                "id": obj.id,
                "pos": obj.loc,
                "color": "black",
                "equipment": []
            }
        return entities_dict
