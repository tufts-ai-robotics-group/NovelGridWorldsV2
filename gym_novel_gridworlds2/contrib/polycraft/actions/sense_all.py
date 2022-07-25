from xmlrpc.client import Boolean
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class SenseAll(Action):
    def __init__(self, state: State, trade=None, dynamics=None):
        self.dynamics = dynamics
        self.state = state

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the SenseAll action:
        1) Does nothing, so return true
        """
        return True

    def do_action(self, agent_entity: Entity, target_object: Object = None):
        """
        Checks for precondition, then gets the metadata
        """
        if agent_entity.facing == "NORTH":
            self.vec = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            self.vec = (1, 0)
        elif agent_entity.facing == "WEST":
            self.vec = (0, -1)
        else:
            self.vec = (0, 1)
        locInFront = tuple(np.add(agent_entity.loc, self.vec))
        objs = self.state.get_objects_at(locInFront)
        if len(objs[0]) > 0:
            self.blockInFront = self.state.nameConversion(objs[0][0].type)
        else:
            self.blockInFront = "minecraft:air"
        self.selectedCount = (
            str(agent_entity.inventory[agent_entity.selectedItem])
            if agent_entity.selectedItem != None
            else str(0)
        )
        e102 = self.state.get_entity_by_id(102)
        self.e102loc = e102.loc
        e103 = self.state.get_entity_by_id(103)
        self.e103loc = e103.loc
        e104 = self.state.get_entity_by_id(104)
        self.e104loc = e104.loc
        self.map_str = ""
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                if self.state._map[(i, j)] is not None:
                    objs = self.state.get_objects_at((i, j))
                    if len(objs[0]) != 0:
                        self.map_str += (
                            '"'
                            + str(72 + objs[0][0].loc[0])
                            + ",17,"
                            + str(64 + objs[0][0].loc[1])
                            + '":'
                            + '{"name": "'
                            + self.state.nameConversion(objs[0][0].type)
                            + '", "isAccessible": true}, '
                        )
                    else:
                        self.map_str += (
                            '"'
                            + str(72 + i)
                            + ",17,"
                            + str(64 + j)
                            + '":'
                            + '{"name": "'
                            + "minecraft:air"
                            + '", "isAccessible": true}, '
                        )
        self.map_str = self.map_str[: len(self.map_str) - 2]
        self.state._step_count += 1
        self.result = "SUCCESS"
        self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        print(
            'b{"blockInFront":{"name":"'
            + self.blockInFront
            + '"}, "inventory":{"0":{"item:"minecraft:log","count":1,"damage":0,"maxdamage":0,"axis":"y","variant":"oak"}'
            '"7":{"item":"minecraft:iron_pickaxe","count":1,"damage":0,"maxdamage":250}'
            '"selectedItem":{"item:"'
            + self.state.nameConversion(agent_entity.selectedItem)
            + '","count":'
            + self.selectedCount
            + "}},"
            '"player":{"pos":['
            + str(72 + agent_entity.loc[0])
            + ",17,"
            + str(64 + agent_entity.loc[1])
            + '],"facing":"'
            + agent_entity.facing
            + '","yaw":280.9509,"pitch":14.849994},"destinationPos":[0,0,0],'
            '"entities":{"103":{"type":"EntityTrader","name":"entity.polycraft.Trader.name",'
            '"id":103,"pos":['
            + str(72 + self.e103loc[0])
            + ",17,"
            + str(64 + self.e103loc[1])
            + '],"color":"black","equipment":[{"itemName":"Sporty Nylon Stockings","itemMeta":0,"count":1},{"itemName":"Sporty Nylon Windbreaker","itemMeta":0,"count":1}]},'
            '"104":{"type":"EntityTrader","name":"entity.polycraft.Trader.name","id":104,"pos":['
            + str(72 + self.e104loc[0])
            + ",17,"
            + str(64 + self.e104loc[1])
            + '],"color":"black","equipment":[]},'
            '"102":{"type":"EntityPogoist","name":"entity.polycraft.Pogoist.name","id":102,"pos":['
            + str(72 + self.e102loc[0])
            + ",17,"
            + str(64 + self.e102loc[1])
            + '],"color":"purple","equipment":[{"itemName":"Noble Pantoble","itemMeta":0,"count":1},{"itemName":"Noble Leggings","itemMeta":0,"count":1},{"itemName":"Noble Gorget","itemMeta":0,"count":1},{"itemName":"Noble Armet","itemMeta":0,"count":1}]}},'
            '"map":{' + self.map_str + '}, "size":[32,1,32],"origin":[72,17,64]},'
            "“goal”: {“goalType”: “ITEM”, “goalAchieved”: "
            + str(self.state.goalAchieved)
            + ", “Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “sense_all”, “argument”: “NONAV”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 114}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
