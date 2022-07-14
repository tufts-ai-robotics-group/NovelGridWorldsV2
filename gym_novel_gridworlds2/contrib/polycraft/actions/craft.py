from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.recipe import Recipe

import numpy as np


class Craft(Action):
    def __init__(self, state: State, recipe, dynamics=None):
        self.state = state
        self.recipe = recipe
        self.itemToCraft = list(recipe["output"][0].keys())[0]

    def check_precondition(
        self, agent_entity: Entity, target_type=None, target_object=None
    ):
        """
        Checks preconditions of the craft action:
        1) The agent must have all of the necessary inputs
        2) The agent must be adjacent to a crafting table if the recipe needs a crafting table
        """
        count = 0
        for item in self.recipe["input"]:
            temp = list(item.keys())
            if temp[0] in agent_entity.inventory:
                if (
                    self.recipe["input"][count][temp[0]]
                    > agent_entity.inventory[temp[0]]
                ):
                    return False  # not enough of the item
            else:
                return False  # one of the inputs isnt in the agents inventory
            count += 1
        if self.recipe["needs_table"] == "False":
            return True
        else:
            return False

    def do_action(self, agent_entity: Entity, target_type=None, target_object=None):
        if not self.check_precondition(agent_entity):
            raise PreconditionNotMetError(
                f"Agent {agent_entity.name} cannot craft {self.itemToCraft}."
            )

        count = 0
        for item in self.recipe["input"]:
            temp = list(item.keys())
            agent_entity.inventory[temp[0]] = (
                agent_entity.inventory[temp[0]] - self.recipe["input"][count][temp[0]]
            )
            count += 1
        if self.itemToCraft in agent_entity.inventory:
            agent_entity.inventory[self.itemToCraft] += self.recipe["output"][0][
                self.itemToCraft
            ]
        else:
            agent_entity.inventory[self.itemToCraft] = self.recipe["output"][0][
                self.itemToCraft
            ]
