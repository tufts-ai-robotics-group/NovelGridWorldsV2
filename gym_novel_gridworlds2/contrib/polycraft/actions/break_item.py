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
        3) If the object is not breakable, the agent must be holding the correct tool
         *  Note that the acted upon function of the respective
            objects can also raise a custom PreconditionNotMetError, which is not 
            necessarily caught here.
        """
        # convert the entity facing direction to coords
        self.temp_loc = self.get_tmp_loc(agent_entity, target_object)
        objs = self.state.get_objects_at(self.temp_loc)
        has_block_obj = False

        for obj in objs[0]:
            if obj.state != "block":
                # pass if no block in front
                continue
            # assumes breakable if all non-floating items are breakable
            is_breakable = getattr(obj, "breakable", True)
            is_breakable_if_holding = getattr(obj, "breakable_holding", [])
            if not is_breakable and is_breakable_if_holding != "all" and \
                        agent_entity.selectedItem not in is_breakable_if_holding:
                if obj is None:
                    obj_type = "air"
                elif hasattr(obj, "type"):
                    obj_type = obj.type
                else:
                    obj_type = target_object.__class__.__name__
                if not is_breakable and is_breakable_if_holding == []:
                    raise PreconditionNotMetError(
                        f'Agent "{agent_entity.nickname}" cannot perform break on {obj_type} because it is unbreakable.'
                    )
                else:
                    raise PreconditionNotMetError(
                        f'Agent "{agent_entity.nickname}" cannot perform break on {obj_type} because it requires tools to be broken.'
                    )
            has_block_obj = True

        if not has_block_obj:
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot perform break because there is nothing in front of it.'
            )

    def do_action(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ) -> str:
        """
        Checks for precondition, then breaks the object
        """
        
        self.check_precondition(agent_entity, target_object)

        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("break", agent_entity)
        if objs[0][0].type == "oak_log" and objs[0][0].state == "floating":
            self.state.tree_was_broken(self.temp_loc)

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
