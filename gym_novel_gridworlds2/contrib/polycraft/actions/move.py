from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

DIRECTION_TO_FACING = {"UP": "NORTH", "DOWN": "SOUTH", "LEFT": "WEST", "RIGHT": "EAST"}


class Move(Action):
    def __init__(self, state: State, dynamics=None, direction="UP"):
        self.direction = direction
        if direction == "UP":
            self.vec = (-1, 0)
        elif direction == "DOWN":
            self.vec = (1, 0)
        elif direction == "LEFT":
            self.vec = (0, -1)
        else:
            self.vec = (0, 1)

        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the move action:
        1) The new location must not be out of bounds
        2) The new location must not be occupied by another non-floating object
        3) If the new location is occupied by a door, it must be open
        """

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

    def do_action(self, agent_entity, target_type=None, target_object=None):
        """
        Checks for precondition, then moves the object to the destination.
        This action should never fail - only the moving part of it should
        """
        print("doing move action")
        agent_entity.facing = DIRECTION_TO_FACING[self.direction]
        new_loc = tuple(np.add(self.vec, agent_entity.loc))
        if self.check_precondition(agent_entity, target_object):
            # multiple objects handling
            objs = self.state.get_objects_at(new_loc)
            if len(objs[0]) != 0:
                for obj in objs[0]:
                    if hasattr(obj, "canWalkOver") and obj.canWalkOver == True:
                        print("peaced it")
                        pass
                    else:
                        if obj.type in agent_entity.inventory:
                            agent_entity.inventory[obj.type] += 1
                        else:
                            agent_entity.inventory[obj.type] = 1
                        self.state.remove_object(obj.type, new_loc)
                        print("dat coca")
            self.state.update_object_loc(agent_entity.loc, new_loc)
            # raise PreconditionNotMetError(f"Cannot move agent {agent_entity.name} from {agent_entity.loc} to {new_loc}")
        else:
            print("beibs")

        # agent_entity.facing = DIRECTION_TO_FACING[self.direction]
