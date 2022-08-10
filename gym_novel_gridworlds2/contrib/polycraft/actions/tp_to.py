from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class TP_TO(Action):
    def __init__(self, state: State, x=None, y=None, entity_id=None, offset=1, dynamics=None, **kwargs):
        super().__init__(state, dynamics, **kwargs)
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.offset = offset
        self.cmd_format = r"tp_to (?P<x>\d+),(?P<z>\d+),(?P<y>\d+) (?P<offset>\d+)"
        self.allow_additional_action = False
        

    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        x=None,
        y=None,
        offset=None,
        **kwargs,
    ):
        x = x if x is not None else self.x
        y = y if y is not None else self.y

        if x != None:
            loc = (int(x), int(y))
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            if ent is not None:
                loc = ent.loc
            else:
                loc = (0, 0)
        """
        Checks preconditions of the TP_TO action:
        1) The spots around the location are unoccupied in the order north, south, east, west
        """

        if loc[0] - offset >= 0:  # ensure not out of bounds
            self.vec = (-offset, 0)
            obj1 = self.state.get_objects_at(np.add(loc, self.vec))  # north
            if len(obj1[0]) != 0:
                if obj1[0][0].state == "floating":
                    agent_entity.facing = "SOUTH"
                    return True
            else:
                if len(obj1[1]) == 0:
                    agent_entity.facing = "SOUTH"
                    return True
        if (
            loc[0] + offset < self.state.initial_info["map_size"][0]
        ):  # ensure not out of bounds
            self.vec = (offset, 0)
            obj2 = self.state.get_objects_at(np.add(loc, self.vec))  # south
            if len(obj2[0]) != 0:
                if obj2[0][0].state == "floating":
                    agent_entity.facing = "NORTH"
                    return True
            else:
                if len(obj2[1]) == 0:
                    agent_entity.facing = "NORTH"
                    return True
        if (
            loc[1] + offset < self.state.initial_info["map_size"][1]
        ):  # ensure not out of bounds
            self.vec = (0, offset)
            obj3 = self.state.get_objects_at(np.add(loc, self.vec))  # east
            if len(obj3[0]) != 0:
                if obj3[0][0].state == "floating":
                    agent_entity.facing = "WEST"
                    return True
            else:
                if len(obj3[1]) == 0:
                    agent_entity.facing = "WEST"
                    return True
        if loc[1] - offset >= 0:  # ensure not out of bounds
            self.vec = (0, -offset)
            obj4 = self.state.get_objects_at(np.add(loc, self.vec))  # west
            if len(obj4[0]) != 0:
                if obj4[0][0].state == "floating":
                    agent_entity.facing = "EAST"
                    return True
            else:
                if len(obj4[1]) == 0:
                    agent_entity.facing = "EAST"
                    return True
        return False

    def do_action(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        x=None,
        y=None,
        z=None,
        offset=None,
        **kwargs,
    ):
        """
        Checks for precondition, then teleports to the location
        """
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        offset = int(offset) if offset is not None else self.offset
        if x != None:
            loc = (int(x), int(y))
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            if ent is not None:
                loc = ent.loc
            else:
                loc = (0, 0)

        self.state.incrementer()
        if not self.check_precondition(
            agent_entity, x=x, y=y, offset=offset, target_object=target_object
        ):
            self.result = "FAILURE"
            self.action_metadata(agent_entity)
            raise PreconditionNotMetError(
                f"Agent {agent_entity.name} cannot teleport to {loc}."
            )
        new_loc = tuple(np.add(self.vec, loc))
        # multiple objects handling
        objs = self.state.get_objects_at(new_loc)
        if len(objs[0]) != 0:
            for obj in objs[0]:
                if (
                    hasattr(obj, "canWalkOver")
                    and obj.canWalkOver == True
                    and obj.state == "block"
                ):
                    pass
                else:
                    if obj.type != "diamond_ore":
                        if obj.type in agent_entity.inventory:
                            agent_entity.inventory[obj.type] += 1
                        else:
                            agent_entity.inventory[obj.type] = 1
                    else:
                        if "diamond" in agent_entity.inventory:
                            agent_entity.inventory["diamond"] += 9
                        else:
                            agent_entity.inventory.update({"diamond": 9})
                    self.state.remove_object(obj.type, new_loc)
        self.state.update_object_loc(agent_entity.loc, new_loc)

        return {}
