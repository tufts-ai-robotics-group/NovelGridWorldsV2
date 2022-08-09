from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np


class ExtractRubber(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the ExtractRubber action:
        1) The agent is facing the object
        2) The object is a tree tap
        3) The object is in block state
        4) The object is adjacent to a tree
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

        correctDirection = False

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1:
            correctDirection = True

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

        return (
            correctDirection
            and adjacentToTree
            and (objs[0][0].type == "tree_tap")
            and (objs[0][0].state == "block")
        )

    def do_action(self, agent_entity: Entity, target_object: Object = None, **kwargs):
        self.state._step_count += 1
        """
        Checks for precondition, then extracts rubber from the object
        """
        if not self.check_precondition(agent_entity, target_object):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot perform use on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("extract_rubber", agent_entity)
