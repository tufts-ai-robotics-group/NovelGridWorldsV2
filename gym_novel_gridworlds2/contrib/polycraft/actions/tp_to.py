from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.coord_convert import external_to_internal

import numpy as np


def find_facing(curr_loc, dst_loc):
    """Find the direction the agent should face to face the destination."""
    if curr_loc is None or dst_loc is None:
        return None
    if curr_loc[0] == dst_loc[0]:
        if curr_loc[1] < dst_loc[1]:
            return 'WEST'
        else:
            return 'EAST'
    elif curr_loc[0] < dst_loc[0]:
        return 'NORTH'
    else:
        return 'SOUTH'


class TP_TO(Action):
    def __init__(self, state: State, x=None, y=None, z=None, entity_id=None, target_obj_type=None, offset=1, dynamics=None, **kwargs):
        super().__init__(state, dynamics, **kwargs)
        self.entity_id = entity_id
        self.target_obj_type = target_obj_type
        self.x = x
        self.y = y
        self.z = z
        self.offset = offset
        self.cmd_format = r"tp_to (?P<x>\d+),(?P<y>\d+),(?P<z>\d+)( (?P<offset>\d+))?"
        self.allow_additional_action = False


    def find_available_spot_around(self, loc, offset, agent_loc=None, curr_room_only=True):
        if loc is None:
            return None
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

    def find_object_of_type(self, obj_type, agent_loc):
        objs = self.state.get_objects_of_type(obj_type)
        found_obj = False
        for obj in objs:
            found_obj = True
            spot = self.find_available_spot_around(obj.loc, 1, agent_loc)
            if spot is not None:
                return True, obj.loc, spot
        return found_obj, None, None


    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: str = None,
        x=None,
        y=None,
        z=None,
        offset=None,
        **kwargs,
    ):
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        z = z if z is not None else self.z

        found_obj = False

        if x != None:
            # mode 1: teleport to a specific location
            loc = external_to_internal((int(x), int(y), int(z)))
            found_obj = True
            loc_w_offset = self.find_available_spot_around(loc, offset, agent_loc=agent_entity.loc)
        elif target_object is not None:
            # mode 2: teleport to an object
            found_obj, loc, loc_w_offset = self.find_object_of_type(target_object, agent_entity.loc)
        else:
            # mode 3: teleport to the location of an entity
            ent = self.state.get_entity_by_id(self.entity_id)
            if ent is not None:
                loc = ent.loc
                found_obj = True
            else:
                loc = None
                found_obj = False
            loc_w_offset = self.find_available_spot_around(loc, offset, agent_loc=agent_entity.loc)
        
        self.tmp_loc = loc_w_offset
        self.tmp_new_facing = find_facing(loc, loc_w_offset) or agent_entity.facing

        if loc_w_offset is None:

            if x is not None:
                target = f"location {(x, y, z)}"
            elif target_object is not None:
                target = f"object {target_object}"
            else:
                target = f"entity {self.entity_id}"
            
            if not found_obj:
                raise PreconditionNotMetError(
                    f"{target} is not found in the world"
                )
            else:
                raise PreconditionNotMetError(
                    f"No available spot around {target}"
                )
        return loc_w_offset

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
        target_object = self.target_obj_type if target_object is None else target_object

        offset = int(offset) if offset is not None else self.offset
        

        new_loc = self.check_precondition(
            agent_entity, x=x, y=y, z=z, offset=offset, target_object=target_object
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
        
        agent_entity.facing = self.tmp_new_facing
        self.state.update_object_loc(agent_entity.loc, new_loc)

        return {}
