from typing import Optional
from gym_novel_gridworlds2.contrib.polycraft.actions.interact import check_target
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.state.recipe_set import Recipe
from gym_novel_gridworlds2.utils.namelogic import backConversion
from .craft import Craft

import numpy as np


class Trade(Craft):
    def __init__(self, min_distance=1, max_distance=3, **kwargs):
        super().__init__(min_distance=1, max_distance=3, **kwargs)
        self.cmd_format = r"\w+ (\d+) *(?: +([\w:]+) (\d+))+"
        self.is_trade = True
        self.min_distance = min_distance
        self.max_distance = max_distance
    
    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        recipe: Optional[Recipe]=None,
        **kwargs,
    ):
        """
        Checks preconditions of the Interact action:
        1) The agent is facing an entity
        2) The entity shares the id with the arg provided
        """

        # make a 3x3 radius around the agent, determine if the wanted entity is there
        near_trader = False
        entity_id = int(kwargs["_all_params"][0]) if "_all_params" in kwargs else None

        near_trader, entity = check_target(agent_entity, self.state, distance_min=self.min_distance, distance_max=self.max_distance)
        if entity_id is not None and entity.id != entity_id:
            # if we specified the trader, but it's not the one we're facing
            near_trader = False
        elif near_trader and entity.id in recipe.entities:
            # if we are facing the trader, and either we did not specify the 
            # trader or it's the one we want
            near_trader = True
            
        return near_trader and \
            super().check_precondition(agent_entity, recipe=recipe)

    def do_action(
        self, agent_entity: Entity, target_type=None, target_object=None, **kwargs
    ):
        if self.itemToCraft is not None:
            recipe = self.recipe_set.get_recipe(self.itemToCraft)
        else:
            if "_all_params" in kwargs:
                input_list = [o for o in kwargs["_all_params"] if o is not None][1:]
                target_object = []
                for i, item in enumerate(input_list):
                    if i % 2 == 0:
                        # backconvert the names
                        target_object.append(backConversion(item))
                    else:
                        # backconvert the quantity
                        target_object.append(item)
            recipe = self.recipe_set.get_recipe_by_input(target_object)
        if recipe is None:
            raise PreconditionNotMetError("wrong recipe")
        
        return super().do_action(agent_entity, target_type, target_object, recipe, **kwargs)
