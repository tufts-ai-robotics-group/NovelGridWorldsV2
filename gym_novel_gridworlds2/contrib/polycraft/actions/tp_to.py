from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.coord_convert import external_to_internal

import numpy as np


class TP_TO(Action):
    def __init__(self, state: State, x=None, y=None, z=None, entity_id=None, offset=1, dynamics=None, **kwargs):
        super().__init__(state, dynamics, **kwargs)
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.offset = offset
        self.cmd_format = r"tp_to (?P<x>\d+),(?P<y>\d+),(?P<z>\d+)( (?P<offset>\d+))?"
        self.allow_additional_action = False


    def find_available_spot(self, loc, offset, agent_loc=None, curr_room_only=True):
        curr_rooms = self.state.get_room_by_loc(agent_loc)
        for dim in range(len(loc)):
            offset_vec = np.zeros(len(loc))
            offset_vec[dim] = offset
            
            # search for + and -
            for mult in [1, -1]:
                new_loc = np.add(loc, mult * offset_vec).astype(int)

                # only teleport to the current room if requested
                dst_in_curr_room = False
                for room in curr_rooms:
                    if new_loc in room:
                        dst_in_curr_room = True
                        break
                
                if not curr_room_only or agent_loc is None or dst_in_curr_room:
                    objs = self.state.get_objects_at(new_loc)
                    if len(objs[1]) == 0:
                        # if there's no entity at the new spot
                        if len(objs[0]) != 0:
                            # if the object there is a block, 
                            # only true when it's floating
                            if objs[0][0].state == "floating":
                                return new_loc
                        else:
                            # if there is no object there and no entity,
                            # it's a valid spot 
                            if len(objs[1]) == 0:
                                return new_loc
        return None
        

    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        x=None,
        y=None,
        z=None,
        offset=None,
        **kwargs,
    ):
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        z = z if z is not None else self.z

        if x != None:
            loc = external_to_internal((int(x), int(y), int(z)))
            print(loc)
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            if ent is not None:
                loc = ent.loc
            else:
                loc = (0, 0)

        loc = self.find_available_spot(loc, offset, agent_loc=agent_entity.loc)
        self.tmp_loc = loc
        return loc is not None

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
        z = z if z is not None else self.z
        offset = int(offset) if offset is not None else self.offset
        if x != None:
            loc = external_to_internal((int(x), int(y), int(z)))
            print(loc)
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            if ent is not None:
                loc = ent.loc
            else:
                loc = (0, 0)

        self.state.incrementer()
        if not self.check_precondition(
            agent_entity, x=x, y=y, z=z, offset=offset, target_object=target_object
        ):
            raise PreconditionNotMetError(
                f"Agent {agent_entity.nickname} cannot teleport to {loc}."
            )
        new_loc = self.tmp_loc
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
