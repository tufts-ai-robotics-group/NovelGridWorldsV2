from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class TP_TO(Action):
    def __init__(self, state: State, x=None, y=None, entity_id=None, dynamics=None):
        self.dynamics = dynamics
        self.state = state
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.cmd_format = "tp_to (?P<x>\d+),(\d+),(?P<y>\d+)"

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        if self.x != None:
            loc = (int(self.x), int(self.y))
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            loc = ent.loc
        """
        Checks preconditions of the TP_TO action:
        1) The spots around the location are unoccupied in the order north, south, east, west
        """

        self.vec = (-1, 0)
        obj1 = self.state.get_objects_at(np.add(loc, (-1, 0)))  # north
        if len(obj1[0]) != 0:
            if obj1[0][0].state == "floating":
                return True
        else:
            if len(obj1[1]) == 0:
                return True
        self.vec = (1, 0)
        obj2 = self.state.get_objects_at(np.add(loc, (1, 0)))  # south
        if len(obj2[0]) != 0:
            if obj2[0][0].state == "floating":
                return True
        else:
            if len(obj2[1]) == 0:
                return True
        self.vec = (0, 1)
        obj3 = self.state.get_objects_at(np.add(loc, (0, 1)))  # east
        if len(obj3[0]) != 0:
            if obj3[0][0].state == "floating":
                return True
        else:
            if len(obj3[1]) == 0:
                return True
        self.vec = (0, -1)
        obj4 = self.state.get_objects_at(np.add(loc, (0, -1)))  # west
        if len(obj4[0]) != 0:
            if obj4[0][0].state == "floating":
                return True
        else:
            if len(obj4[1]) == 0:
                return True
        return False

    def do_action(self, agent_entity: Entity, target_object: Object = None, x=None, y=None):
        """
        Checks for precondition, then teleports to the location
        """
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        if x != None:
            loc = ((int(x), int(y)))
        else:
            ent = self.state.get_entity_by_id(self.entity_id)
            loc = ent.loc
        
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity):
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

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        # TODO Update self.x, y, z to actual coord
        if self.x != None:
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “tp_to”, “argument”: “"
                + str(self.x)
                + ",17,"
                + str(self.y)
                + "”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 282.72424}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        else:
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “tp_to”, “argument”: “"
                + str(self.entity_id)
                + "”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 282.72424}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
