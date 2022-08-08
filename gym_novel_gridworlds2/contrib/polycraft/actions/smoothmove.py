from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class SmoothMove(Action):
    def __init__(self, direction="W", **kwargs):
        self.direction = direction
        self.vec = (0, 0)
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
            if self.direction == "W":
                self.vec = (-1, 0)
            elif self.direction == "S":
                self.vec = (1, 0)
            elif self.direction == "A":
                self.vec = (0, -1)
            else:
                self.vec = (0, 1)
        elif agent_entity.facing == "EAST":
            if self.direction == "W":
                self.vec = (0, 1)
            elif self.direction == "S":
                self.vec = (0, -1)
            elif self.direction == "A":
                self.vec = (-1, 0)
            else:
                self.vec = (1, 0)
        elif agent_entity.facing == "WEST":
            if self.direction == "W":
                self.vec = (0, -1)
            elif self.direction == "S":
                self.vec = (0, 1)
            elif self.direction == "A":
                self.vec = (1, 0)
            else:
                self.vec = (-1, 0)
        else:
            if self.direction == "W":
                self.vec = (1, 0)
            elif self.direction == "S":
                self.vec = (-1, 0)
            elif self.direction == "A":
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

    def do_action(self, agent_entity, target_type=None, target_object=None):
        self.state.incrementer()
        """
        Checks for precondition, then moves the object to the destination.
        """
        if self.check_precondition(agent_entity, target_object):
            new_loc = tuple(np.add(self.vec, agent_entity.loc))
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
            self.result = "SUCCESS"
        else:
            self.result = "FAILED"

        return self.action_metadata(agent_entity, target_object)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        return "".join(
            "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: '"
            + str(self.state.goalAchieved)
            + ", “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “smooth_move”, “argument”: “"
            + self.direction
            + "”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 27.906975}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
