from typing import List
import numpy as np
from gym_novel_gridworlds2.contrib.polycraft.states import PolycraftState
from gym_novel_gridworlds2.object.entity import Entity

from gym_novel_gridworlds2.state.state import State
from gym_novel_gridworlds2.state.dynamic import Dynamic

def getBlockInFront(agent_entity, state: PolycraftState):
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


def getInventory(agent_entity: Entity):
    inventory = {
        str(slot_id): {
            "item": item_name,
            "count": count,
            "damage": 0,
            "maxdamage": 0
        } for slot_id, (item_name, count) in enumerate(agent_entity.inventory.items())
    }

    # todo check if correct
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


def getEntities(state: PolycraftState):
    all_entities: List[Entity] = state.get_all_entities()
    return {
        str(obj.id): {
            "type": obj.__class__.__name__,
            "name": obj.name,
            "id": obj.id,
            "pos": obj.loc,
            "color": "black",
            "equipment": []
        } for obj in all_entities
    }
        


def sense_all(agent_entity: Entity, state: PolycraftState, dynamic: Dynamic):
    return {
        "blockInFront": {
            "name": getBlockInFront(agent_entity, state)
        },
        "inventory": getInventory(agent_entity),
        "player": {
            "pos": agent_entity.loc,
            "facing": agent_entity.facing,
            "yaw": 90.0,  # dummy
            "pitch": 0.0  # dummy
        },
        "destinationPos": [0, 0, 0],
        "entities": getEntities(),
        "map": {
            "blocks": list(state.get_map_rep_in_type().reshape(-1)),
            "size": state.get_map_size(),
            "origin": [0, 0, 0]
        },
    }