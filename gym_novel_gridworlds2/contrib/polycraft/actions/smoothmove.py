from gym_novel_gridworlds2.contrib.polycraft.utils.inventory_utils import collect_item
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class SmoothMove(Action):
    def __init__(self, direction=None, **kwargs):
        self.direction = direction
        self.vec = (0, 0)
        self.cmd_format = r"\w+ (?P<direction>\w+)"
        super().__init__(**kwargs)
        
    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the smooth_move action:
        1) The new location must not be out of bounds
        2) The new location must not be occupied by another non-floating object
        3) If the new location is occupied by a door, it must be open
        """

        if agent_entity.facing == "NORTH":
            if self.direction_tmp == "W":
                self.vec = (-1, 0)
            elif self.direction_tmp == "X":
                self.vec = (1, 0)
            elif self.direction_tmp == "A":
                self.vec = (0, -1)
            else:
                self.vec = (0, 1)
        elif agent_entity.facing == "EAST":
            if self.direction_tmp == "W":
                self.vec = (0, 1)
            elif self.direction_tmp == "X":
                self.vec = (0, -1)
            elif self.direction_tmp == "A":
                self.vec = (-1, 0)
            else:
                self.vec = (1, 0)
        elif agent_entity.facing == "WEST":
            if self.direction_tmp == "W":
                self.vec = (0, -1)
            elif self.direction_tmp == "X":
                self.vec = (0, 1)
            elif self.direction_tmp == "A":
                self.vec = (1, 0)
            else:
                self.vec = (-1, 0)
        else:
            if self.direction_tmp == "W":
                self.vec = (1, 0)
            elif self.direction_tmp == "X":
                self.vec = (-1, 0)
            elif self.direction_tmp == "A":
                self.vec = (0, 1)
            else:
                self.vec = (0, -1)

        new_loc = np.add(self.vec, agent_entity.loc)
        # check for bounds
        if (new_loc >= 0).all() and (new_loc < self.state._map.shape).all():
            # if it's inside the bounds
            obj = self.state.get_object_at(tuple(new_loc))
            if obj is not None:
                # check if object is floating or not.
                # if floating, still able to pass thru
                # if block, cannot pass thru unless door
                if not hasattr(obj, "state") or obj.state == "block":
                    if not hasattr(obj, "canWalkOver") or obj.canWalkOver == False:
                        return False
            return True
        else:
            # out of the bound
            return False

    def do_action(self, agent_entity, target_type=None, target_object=None, direction=None, **kwargs):
        """
        Checks for precondition, then moves the object to the destination.
        """
        

        if self.direction is None:
            if direction is None:
                direction = "W"
            self.direction_tmp = direction.upper()
        else:
            self.direction_tmp = self.direction

        if self.check_precondition(agent_entity, target_object):
            new_loc = tuple(np.add(self.vec, agent_entity.loc))
            # multiple objects handling
            objs = self.state.get_objects_at(new_loc)
            if len(objs[0]) != 0:
                # iterate through and remove every non-block element
                # at the new location
                i = 0
                while i != len(objs[0]):
                    obj = objs[0][i]
                    if not (
                        getattr(obj, "canWalkOver", False)
                        and obj.state == "block"
                    ):
                        collect_item(self.state, agent_entity, obj, new_loc)
                    else:
                        # not removing the current block, increment current index
                        i += 1
            self.state.update_object_loc(agent_entity.loc, new_loc)
        else:
            raise PreconditionNotMetError()

        return {}
