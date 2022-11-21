from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class Break(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_tmp_loc(self, agent_entity: Entity, target_type: str = None, target_object: PolycraftObject = None, *args, **kwargs):
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
        Checks preconditions of the break action:
        1) The agent is facing an object
        2) The object is breakable
        """
        # convert the entity facing direction to coords
        correctDirection = False

        self.temp_loc = self.get_tmp_loc(agent_entity, target_object)
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1:
            correctDirection = True
            unbreakableObjects = ["bedrock", "plastic_chest", "safe", "unlocked_safe"]
            if objs[0][0].type in unbreakableObjects:
                return False
        elif len(objs[0]) == 0:
            # cannot break air
            return False

        return correctDirection and (objs[0][0].state == "block")

    def do_action(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ) -> str:
        """
        Checks for precondition, then breaks the object
        """
        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_object):
            self.result = "FAILED"
            self.action_metadata(agent_entity, target_object)

            if target_object is None:
                obj_type = "air"
            elif hasattr(target_object, "type"):
                obj_type = target_object.type
            else:
                obj_type = target_object.__class__.__name__

            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot perform break on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("break", agent_entity)
        if objs[0][0].type == "oak_log" and objs[0][0].state == "floating":
            self.state.tree_was_broken(self.temp_loc)

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity, target_object)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        return {}
    
    def get_step_cost(self, agent_entity: Entity, target_type: str = None, target_object: PolycraftObject = None, *args, **kwargs):
        temp_loc = self.get_tmp_loc(agent_entity, target_object)
        # returns special break cost or default cost depending on object type
        objs = self.state.get_objects_at(temp_loc)[0]
        if (len(objs)) == 0:
            return 0
        return getattr(objs[0], "break_cost", self.step_cost)
