from typing import Optional
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

from gym_novel_gridworlds2.state.recipe import Recipe, RecipeSet

from gym_novel_gridworlds2.utils import nameConversion, backConversion


class Craft(Action):
    def __init__(
        self,
        recipe_set: RecipeSet,
        recipe_name: Optional[str] = None,
        default_step_cost: int = 100,
        **kwargs,
    ):
        self.recipe_set = recipe_set
        self.itemToCraft = recipe_name
        self.cmd_format = r"\w+ 1 ([:\w]+) ([:\w]+) ([:\w]+) ([:\w]+)(?: ([:\w]+) ([:\w]+) ([:\w]+) ([:\w]+) ([:\w]+))?"
        self.default_step_cost = default_step_cost
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the craft action:
        1) The agent must have all of the necessary inputs
        2) The agent must be adjacent to a crafting table if the recipe needs a crafting table
        """
        # legacy support
        if self.itemToCraft is not None:
            recipe = self.recipe_set.get_recipe(self.itemToCraft)
        else:
            recipe = self.recipe_set.get_recipe_by_input(target_object)

        if recipe is None:
            print("available recipes:", self.recipe_set.recipe_index.keys())
            raise PreconditionNotMetError("recipe is wrong.")

        for item, count in recipe.input_dict.items():
            if item == "0":
                # empty slot, skip
                continue
            if item in agent_entity.inventory:
                if count > agent_entity.inventory[item]:
                    return False  # not enough of the item
            else:
                return False  # one of the inputs isnt in the agents inventory
        if len(recipe.input_list) <= 4 or recipe.input_list[4] is None:
            # if input_list is <= 4 items long,
            # which means it does not require crafting table
            return True
        else:
            return self.is_near_crafting_table(agent_entity)

    def is_near_crafting_table(self, agent_entity):
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
        if len(objs[0]) == 1:
            if objs[0][0].type == "crafting_table":
                return True
            else:
                return False

    def do_action(
        self, agent_entity: Entity, target_type=None, target_object=None, **kwargs
    ):
        if "_all_params" in kwargs:
            input_list = [o for o in kwargs["_all_params"] if o is not None]
            target_object = [backConversion(o) for o in input_list]

        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_type, target_object):
            raise PreconditionNotMetError(
                f"Agent {agent_entity.nickname} cannot craft {self.itemToCraft}."
            )

        if self.itemToCraft is not None:
            recipe = self.recipe_set.get_recipe(self.itemToCraft)
        else:
            recipe = self.recipe_set.get_recipe_by_input(target_object)

        for item, count in recipe.input_dict.items():
            if item != "0":
                agent_entity.inventory[item] -= count

        for item, quantity in recipe.output_dict.items():
            if item is not None:
                if item in agent_entity.inventory:
                    agent_entity.inventory[item] += quantity
                else:
                    agent_entity.inventory[item] = quantity

        if self.itemToCraft == "pogo_stick" or "pogo_stick" in recipe.output_dict:
            self.state.goalAchieved = True
        return self.action_metadata(kwargs, recipe=recipe)

    def action_metadata(self, args=[], recipe: Optional[Recipe] = None):
        if self.itemToCraft is not None:
            return {
                "command_result": {
                    "command": args.get('_command') or "craft",
                    "argument": self.itemToCraft,
                    "message": "",
                    "result": "SUCCESS",
                    "stepCost": self.recipe_set.get_recipe(self.itemToCraft).step_cost,
                }
            }
        else:
            return {
                "command_result": {
                    "command": args['_command'],
                    "argument": args['_raw_args'],
                    "message": "",
                    "result": "SUCCESS",
                    "stepCost": recipe.step_cost,
                }
            }
