from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np


def can_interact(agent_entity, state, entity_id):
    if agent_entity.loc[0] - 1 >= 0:
        temp_loc = tuple(np.add(agent_entity.loc, (-1, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[0] - 2 >= 0:
        temp_loc = tuple(np.add(agent_entity.loc, (-2, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[0] - 3 >= 0:
        temp_loc = tuple(np.add(agent_entity.loc, (-3, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True

    if agent_entity.loc[0] + 1 < state.initial_info["map_size"][0]:
        temp_loc = tuple(np.add(agent_entity.loc, (1, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[0] + 2 < state.initial_info["map_size"][0]:
        temp_loc = tuple(np.add(agent_entity.loc, (2, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[0] + 3 < state.initial_info["map_size"][0]:
        temp_loc = tuple(np.add(agent_entity.loc, (3, 0)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True

    if agent_entity.loc[1] + 1 < state.initial_info["map_size"][1]:
        temp_loc = tuple(np.add(agent_entity.loc, (0, 1)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[1] + 2 < state.initial_info["map_size"][1]:
        temp_loc = tuple(np.add(agent_entity.loc, (0, 2)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[1] + 3 < state.initial_info["map_size"][1]:
        temp_loc = tuple(np.add(agent_entity.loc, (0, 3)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[1] - 1 > 0:
        temp_loc = tuple(np.add(agent_entity.loc, (0, -1)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[1] - 2 > 0:
        temp_loc = tuple(np.add(agent_entity.loc, (0, -2)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    if agent_entity.loc[1] - 3 > 0:
        temp_loc = tuple(np.add(agent_entity.loc, (0, -3)))
        objs = state.get_objects_at(temp_loc)
        if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
            if entity_id == objs[1][0].id:
                return True
    return False


class Interact(Action):
    def __init__(self, entity_id=None, **kwargs):
        self.entity_id = entity_id
        self.cmd_format = r"\w+ (?P<entity_id>\w+)"
        super().__init__(**kwargs)

    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        entity_id=None,
        **kwargs,
    ):
        """
        Checks preconditions of the Interact action:
        1) The agent is facing an entity
        2) The entity shares the id with the arg provided
        """

        # make a 3x3 radius around the agent, determine if the wanted entity is there
        if entity_id is None:
            return False
        entity_id = int(entity_id)

        return can_interact(agent_entity, self.state, entity_id)

    def do_action(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        entity_id=None,
        **kwargs,
    ):
        """
        Checks for precondition, then interacts with the entity
        """
        if entity_id is None:
            entity_id = self.entity_id
        self.state.incrementer()
        if not self.check_precondition(
            agent_entity, target_object, entity_id=entity_id
        ):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot perform use on {obj_type}.'
            )

        return self.action_metadata(agent_entity, target_object, entity_id=entity_id)

    def action_metadata(
        self, agent_entity, target_type=None, target_object=None, entity_id=None
    ):
        entity_id = int(entity_id)
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
