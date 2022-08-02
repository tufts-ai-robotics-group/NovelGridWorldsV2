from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


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

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then does nothing
        """
        # self.state._step_count += 1
        self.state.incrementer()
        self.result = "SUCCESS"
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        return "".join(
            'b\'"{"recipes":[{"inputs":[{"Item":"minecraft:planks","stackSize":1,"slot":0}, \
            {"Item":"minecraft:stick","stackSize":1,"slot":1},{"Item":"minecraft:planks","stackSize":1,"slot":2},\
            {"Item":"minecraft:planks","stackSize":1,"slot":3},{"Item":"minecraft:planks","stackSize":1,"slot":5}, \
            {"Item":"minecraft:planks","stackSize":1,"slot":7}],"outputs":[{"Item":"polycraft:tree_tap","stackSize":1,"slot":9}]}, \
            {"inputs":[{"Item":"minecraft:stick","stackSize":1,"slot":0},{"Item":"polycraft:block_of_titanium","stackSize":1,"slot":1}, \
            {"Item":"minecraft:stick","stackSize":1,"slot":2},{"Item":"minecraft:diamond_block","stackSize":1,"slot":3}, \
            {"Item":"polycraft:block_of_titanium","stackSize":1,"slot":4},{"Item":"minecraft:diamond_block","stackSize":1,"slot":5}, \
            {"Item":"polycraft:sack_polyisoprene_pellets","stackSize":1,"slot":7}],"outputs":[{"Item":"polycraft:wooden_pogo_stick","stackSize":1,"slot":9}]}, \
            {"inputs":[{"Item":"minecraft:log","stackSize":1,"slot":-1}],"outputs":[{"Item":"minecraft:planks","stackSize":4,"slot":9}]}, \
            {"inputs":[{"Item":"minecraft:planks","stackSize":1,"slot":0},{"Item":"minecraft:planks","stackSize":1,"slot":3}], \
            "outputs":[{"Item":"minecraft:stick","stackSize":4,"slot":9}]},{"inputs":[{"Item":"minecraft:planks","stackSize":1,"slot":0}, \
            {"Item":"minecraft:planks","stackSize":1,"slot":1},{"Item":"minecraft:planks","stackSize":1,"slot":3}, \
            {"Item":"minecraft:planks","stackSize":1,"slot":4}],"outputs":[{"Item":"minecraft:crafting_table","stackSize":1,"slot":9}]}, \
            {"inputs":[{"Item":"minecraft:diamond","stackSize":1,"slot":0},{"Item":"minecraft:diamond","stackSize":1,"slot":1}, \
            {"Item":"minecraft:diamond","stackSize":1,"slot":2},{"Item":"minecraft:diamond","stackSize":1,"slot":3},{"Item":"minecraft:diamond","stackSize":1,"slot":4}, \
            {"Item":"minecraft:diamond","stackSize":1,"slot":5},{"Item":"minecraft:diamond","stackSize":1,"slot":6},{"Item":"minecraft:diamond","stackSize":1,"slot":7}, \
            {"Item":"minecraft:diamond","stackSize":1,"slot":8}],"outputs":[{"Item":"minecraft:diamond_block","stackSize":1,"slot":9}]}],"goal":{"goalType":"ITEM","goalAchieved":false,"Distribution":"Uninformed"}, \
            "command_result":{"command":"sense_recipes","argument":"","result":"SUCCESS","message":"","stepCost":1200.0},"step":2,"gameOver":false}\n'
            "{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “sense_recipes”, “argument”: “”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 120}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
