from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.utils import nameConversion
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

from gym_novel_gridworlds2.state.recipe import RecipeSet


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
            output.append(
                {
                    "inputs": [
                        {"Item": nameConversion(item), "stackSize": 1, "slot": i}
                        for i, item in enumerate(recipe.input_list)
                        if item is not None and item != "0"
                    ],
                    "outputs": [
                        {"Item": nameConversion(item), "stackSize": 1, "slot": i}
                        for i, item in enumerate(recipe.output_list)
                        if item is not None and item != "0"
                    ],
                }
            )
        return {"recipes": output}
