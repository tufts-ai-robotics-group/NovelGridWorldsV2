from gym_novel_gridworlds2.contrib.polycraft.states.polycraft_state import (
    PolycraftState,
)
from gym_novel_gridworlds2.object.entity import Entity, Object
import numpy as np

def getBlockInFront(agent_entity, state: PolycraftState, nameConversion=None):
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
        if nameConversion is not None:
            name, properties = nameConversion(obj.type, obj=obj)
        else:
            name, properties = obj.type, {}
        blockInFront = {
            "name": name,
            # TODO generalize; also see polycraft_state
            **properties
        }
    else:
        blockInFront = {"name": "air"}
    return blockInFront
