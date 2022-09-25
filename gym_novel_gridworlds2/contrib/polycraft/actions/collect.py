from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class Collect(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_tmp_loc(self, agent_entity: Entity, target_type: str = None, target_object = None, *args, **kwargs):
        # returns temporary location of object
        direction = (0, 0)
        if agent_entity.facing == "NORTH":
            direction = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            direction = (1, 0)
        elif agent_entity.facing == "EAST":
            direction = (0, 1)
        else:
            direction = (0, -1)

        temp_loc = tuple(np.add(agent_entity.loc, direction))
        return temp_loc

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the Collect action:
        1) The agent is facing the object
        2) The object is a tree tap or a safe
        3) The object is in block state
        4) If the object is a tree tap, it should be adjacent to a tree
        5) If the object is a safe, it should be unlocked
        """
        # convert the entity facing direction to coords
        direction = (0, 0)
        if agent_entity.facing == "NORTH":
            direction = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            direction = (1, 0)
        elif agent_entity.facing == "EAST":
            direction = (0, 1)
        else:
            direction = (0, -1)

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        # there is no object to collect from
        if len(objs[0]) != 1:
            return False

        if objs[0][0].type == "tree_tap":

            adjacentToTree = False

            obj1 = self.state.get_objects_at(np.add(self.temp_loc, (0, -1)))
            if len(obj1[0]) == 1:
                if obj1[0][0].type == "oak_log" and obj1[0][0].state == "block":
                    adjacentToTree = True
            obj2 = self.state.get_objects_at(np.add(self.temp_loc, (0, 1)))
            if len(obj2[0]) == 1:
                if obj2[0][0].type == "oak_log" and obj2[0][0].state == "block":
                    adjacentToTree = True
            obj3 = self.state.get_objects_at(np.add(self.temp_loc, (1, 0)))
            if len(obj3[0]) == 1:
                if obj3[0][0].type == "oak_log" and obj3[0][0].state == "block":
                    adjacentToTree = True
            obj4 = self.state.get_objects_at(np.add(self.temp_loc, (-1, 0)))
            if len(obj4[0]) == 1:
                if obj4[0][0].type == "oak_log" and obj4[0][0].state == "block":
                    adjacentToTree = True

            return adjacentToTree and (objs[0][0].state == "block")
        elif objs[0][0].type == "unlocked_safe":
            return (objs[0][0].isLocked == False) and (objs[0][0].state == "block")
        else:
            return objs[0][0].state == "block"

    def do_action(self, agent_entity: Entity, target_object: Object = None, **kwargs):
        """
        Checks for precondition, then collects from the object
        """
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_object):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot perform use on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("collect", agent_entity)

        self.result = "SUCCESS"
        return {}
    
    def get_step_cost(self, agent_entity: Entity, target_type: str = None, target_object = None, *args, **kwargs):
        temp_loc = self.get_tmp_loc(agent_entity, target_object)
        # returns special break cost or default cost depending on object type
        objs = self.state.get_objects_at(temp_loc)[0]
        if (len(objs)) == 0:
            return 0
        return getattr(objs[0], "collect_cost", self.step_cost)