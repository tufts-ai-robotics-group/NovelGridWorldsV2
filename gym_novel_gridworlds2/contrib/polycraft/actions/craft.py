from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.recipe import Recipe

import numpy as np

class Craft(Action):
    def __init__(self, state: State, recipe, dynamics=None):
        self.state = state
        temp = list(recipe.keys())
        self.recipe = recipe
        self.itemToCraft = temp[0]
        self.inputs = recipe[temp[0]]["input"]
        self.outputs = recipe[temp[0]]["output"]
        #perhaps there are multiple ways to craft stuff

    def check_precondition(self, agent_entity: Entity, target_type=None, target_object=None):
        """
        Checks preconditions of the craft action: 
        1) The agent must have all of the necessary inputs
        2) The agent must be adjacent to a crafting table
        """
        count = 0
        for item in self.inputs:
            temp = list(item.keys())
            if temp[0] in agent_entity.inventory:
                    if self.recipe[self.itemToCraft]["input"][count][temp[0]] > agent_entity.inventory[temp[0]]: 
                        return False #not enough of the item 
            else:
                return False #one of the inputs isnt in the agents inventory
            count = count + 1
        return True

    def do_action(self, agent_entity: Entity, target_type=None, target_object=None):
        if not self.check_precondition(agent_entity):
            raise PreconditionNotMetError(f"Agent {agent_entity.name} cannot craft {self.itemToCraft}.")

        count = 0
        for item in self.inputs:
            temp = list(item.keys())
            agent_entity.inventory[temp[0]] = agent_entity.inventory[temp[0]] - self.recipe[self.itemToCraft]["input"][count][temp[0]]
            count = count + 1
        if self.itemToCraft in agent_entity.inventory:
            agent_entity.inventory[self.itemToCraft] = agent_entity.inventory[self.itemToCraft] + self.recipe[self.itemToCraft]["output"][0][self.itemToCraft]
        else:
            agent_entity.inventory[self.itemToCraft] = self.recipe[self.itemToCraft]["output"][0][self.itemToCraft]

