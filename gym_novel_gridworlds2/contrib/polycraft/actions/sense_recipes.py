from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

from gym_novel_gridworlds2.state.recipe_set import RecipeSet

def convert_input_slot_id(old_id, needs_shifting):
    """
    Shifts the slot id to the right by 1 if using simple 2x2 crafting grid
    """
    if needs_shifting and old_id >= 2:
        return old_id + 1
    else:
        return old_id


class SenseRecipes(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_additional_action = True

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the SenseRecipes action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, target_object: Object = None, **kwargs):
        """
        Checks for precondition, then does nothing
        """
        # self.state._step_count += 1
        self.state.incrementer()
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        recipe_set: RecipeSet = self.dynamics.recipe_set
        output = []
        for recipe in recipe_set.recipes.values():

            # for recipes only involing four slots of the crafting grid
            # the slots used are 0, 1, 3, 4. shift the last two input slots by 1
            need_input_shift = len(recipe.input_list) <= 4

            # add all non-empty slots to the input list
            output.append(
                {
                    "inputs": [
                        {
                            "Item": nameConversion(item)[0], 
                            "stackSize": 1, 
                            "slot": convert_input_slot_id(i, need_input_shift)
                        } for i, item in enumerate(recipe.input_list)
                          if item is not None and item != "0"
                    ],
                    "outputs": [
                        {
                            "Item": nameConversion(item)[0], 
                            "stackSize": quantity, 
                            "slot": 9 - i
                        } for i, (item, quantity) in enumerate(recipe.output_dict.items())
                          if item is not None and item != "0"
                    ],
                }
            )
        return {"recipes": output}
