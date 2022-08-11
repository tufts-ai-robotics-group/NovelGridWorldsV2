from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np


class Interact(Action):
    def __init__(self, entity_id=None, **kwargs):
        self.entity_id = entity_id
        self.cmd_format = r"\w+ (?P<entity_id>\w+)"
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, entity_id=None, **kwargs
    ):
        """
        Checks preconditions of the Interact action:
        1) The agent is facing an entity
        2) The entity shares the id with the arg provided
        """
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
        if len(objs[1]) != 1:
            return False

        if hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
        else:
            return False

    def do_action(self, agent_entity: Entity, target_object: Object = None, entity_id=None, **kwargs):
        """
        Checks for precondition, then interacts with the entity
        """
        if entity_id is None:
            entity_id = self.entity_id
        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_object, entity_id=entity_id):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot perform use on {obj_type}.'
            )
        # objs = self.state.get_objects_at(self.temp_loc)
        # if objs[1][0].type == "trader":
        #     # get its inventory, print out trades respective to that
        #     for item in objs[1][0].inventory:
        #         print("trade_" + item)

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