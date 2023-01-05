from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.contrib.polycraft.actions.interact import Interact

import numpy as np


class InteractSupplier(Interact):
    def __init__(self, entity_id=None, **kwargs):
        super().__init__(entity_id, **kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, entity_id=None, **kwargs
    ):
        super().check_precondition(agent_entity, target_object, entity_id, **kwargs)

    def do_action(self, agent_entity: Entity, target_object: Object = None, entity_id=None, **kwargs):
        """
        Checks for precondition, then interacts with the entity
        """
        super().do_action(agent_entity, target_object, entity_id, **kwargs)

        objs = self.state.get_objects_at(self.temp_loc)
        if objs[1][0].type == "trader":
            # get its inventory, print out trades respective to that
            for item in objs[1][0].inventory:
                print("trade_" + item)

        if objs[1][0].id == 106:
            # print("Interacting with supplier.")
            for item in objs[1][0].inventory:
                if item in agent_entity.inventory:
                    agent_entity.inventory[item] += objs[1][0].inventory[item]
                else:
                    agent_entity.inventory[item] = objs[1][0].inventory[item]
                objs[1][0].inventory[item] = 0
                break

        return self.action_metadata(agent_entity, target_object, entity_id=entity_id)

    def action_metadata(self, agent_entity, target_type=None, target_object=None, entity_id=None):
        if entity_id == 103:
            return {
                "trades": {
                    "trades": [
                        {
                            "inputs": [
                                {
                                    "Item": "polycraft:block_of_platinum",
                                    "stackSize": 1,
                                    "slot": 0,
                                }
                            ],
                            "outputs": [
                                {
                                    "Item": "polycraft:block_of_titanium",
                                    "stackSize": 1,
                                    "slot": 5,
                                }
                            ],
                        },
                        {
                            "inputs": [
                                {
                                    "Item": "minecraft:diamond",
                                    "stackSize": 18,
                                    "slot": 0,
                                }
                            ],
                            "outputs": [
                                {
                                    "Item": "polycraft:block_of_platinum",
                                    "stackSize": 1,
                                    "slot": 5,
                                }
                            ],
                        },
                    ]
                },
            }
        elif entity_id == 104:
            return {
                "trades": {
                    "trades": [
                        {
                            "inputs": [
                                {
                                    "Item": "polycraft:block_of_platinum",
                                    "stackSize": 2,
                                    "slot": 0,
                                }
                            ],
                            "outputs": [
                                {"Item": "minecraft:diamond", "stackSize": 9, "slot": 5}
                            ],
                        },
                        {
                            "inputs": [
                                {"Item": "minecraft:log", "stackSize": 10, "slot": 0}
                            ],
                            "outputs": [
                                {
                                    "Item": "polycraft:block_of_titanium",
                                    "stackSize": 1,
                                    "slot": 5,
                                }
                            ],
                        },
                    ]
                },
            }
        else:
            return {}
        # print(
        #     "“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
        #         “command_result”: {“command”: “interact”, “argument”: “"
        #     + str(self.entity_id)
        #     + "”, “result”: "
        #     + self.result
        #     + ", \
        #         “message”: “”, “stepCost: 282.72424}, “step”: "
        #     + str(self.state._step_count)
        #     + ", “gameOver”:false}"
        # )
        # return {} # TODO UPDATE