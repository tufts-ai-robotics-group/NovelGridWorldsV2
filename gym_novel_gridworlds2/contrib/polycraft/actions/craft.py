from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.utils.recipe import Recipe

import numpy as np


class Craft(Action):
    def __init__(self, recipe, **kwargs):
        self.itemToCraft = list(recipe["output"][0].keys())[0]
        super().__init__(**kwargs)

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
        if "needs_table" not in self.recipe or self.recipe["needs_table"] == "False":
            return True
        else:
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
                if objs[0][0].type == "crafting_table":
                    return True
                else:
                    return False

    def do_action(self, agent_entity: Entity, target_type=None, target_object=None):
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity):
            self.result = "FAILED"
            self.action_metadata(agent_entity)
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

        self.result = "SUCCESS"
        if self.itemToCraft == "pogo_stick":
            self.state.goalAchieved = True
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        if self.itemToCraft == "plank":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “craft”, “argument”: “1 Minecraft:log 0 0 0”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 1200}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToCraft == "stick":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “craft”, “argument”: “1 Minecraft:planks 0 Minecraft:planks 0”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 2400}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToCraft == "tree_tap":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “craft”, “argument”: “1 Minecraft:planks Minecraft:stick Minecraft:planks Minecraft:planks 0 Minecraft:planks 0 Minecraft:planks 0”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 7200}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToCraft == "block_of_diamond":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “craft”, “argument”: “1 minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond minecraft:diamond”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 10800}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToCraft == "pogo_stick":
            return "".join(
                "{“goal”: {“goalType”: “ITEM”, “goalAchieved”: true, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “craft”, “argument”: “1 minecraft:stick polycraft:block_of_titanium minecraft:stick minecraft:diamond_block polycraft:block_of_titanium minecraft:diamond_block 0 polycraft:sack_polyisoprene_pellets 0”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 8400}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
