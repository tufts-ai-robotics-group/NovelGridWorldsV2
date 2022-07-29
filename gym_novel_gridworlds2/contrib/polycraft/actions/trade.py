from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class Trade(Action):
    def __init__(self, state: State, trade=None, dynamics=None):
        self.dynamics = dynamics
        self.state = state
        self.trade = trade
        self.itemToTrade = list(trade["output"][0].keys())[0]

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the trade action:
        1) The agent is facing an entity of type trader
        2) The trader has the item to trade
        3) The agent must have all of the necessary inputs
        """
        count = 0
        for item in self.trade["input"]:
            temp = list(item.keys())
            if temp[0] in agent_entity.inventory:
                if (
                    self.trade["input"][count][temp[0]]
                    > agent_entity.inventory[temp[0]]
                ):
                    return False  # not enough of the item
            else:
                return False  # one of the inputs isnt in the agents inventory
            count += 1
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
        if len(objs[1]) == 1:
            if objs[1][0].type == "trader":
                if self.itemToTrade in objs[1][0].inventory:
                    correctDirection = True

        return correctDirection

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then trades for the item
        """
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity):
            self.result = "FAILED"
            self.action_metadata(agent_entity)
            raise PreconditionNotMetError(
                f"Agent {agent_entity.name} cannot trade for {self.itemToTrade}."
            )

        count = 0
        for item in self.trade["input"]:
            temp = list(item.keys())
            agent_entity.inventory[temp[0]] = (
                agent_entity.inventory[temp[0]] - self.trade["input"][count][temp[0]]
            )
            count += 1
        if self.itemToTrade in agent_entity.inventory:
            agent_entity.inventory[self.itemToTrade] += self.trade["output"][0][
                self.itemToTrade
            ]
        else:
            agent_entity.inventory[self.itemToTrade] = self.trade["output"][0][
                self.itemToTrade
            ]

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        if self.itemToTrade == "block_of_titanium":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “trade”, “argument”: “103 polycraft:block_of_platinum 1”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 1200}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToTrade == "block_of_platinum":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “trade”, “argument”: “103 minecraft:diamond 18”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 20400}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
        elif self.itemToTrade == "diamond":
            return "".join(
                "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: false, “Distribution”: “Uninformed”}, \
                “command_result”: {“command”: “trade”, “argument”: “104 polycraft:block_of_platinum 2”, “result”: "
                + self.result
                + ", \
                “message”: “”, “stepCost: 2400}, “step”: "
                + str(self.state._step_count)
                + ", “gameOver”:false}"
            )
