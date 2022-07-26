import enum
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

        self.selected_item_str = (
            '"selectedItem":{"item:"'
            + self.state.nameConversion(agent_entity.selectedItem)
            + '","count":'
            + self.selectedCount
            + ',"damage":0,"maxdamage":0'
        )
        if agent_entity.selectedItem == "oak_log":
            self.selected_item_str += ',"axis":"y","variant":"oak"}}'
        else:
            self.selected_item_str += "}},"

        self.inventory_str = '"inventory":{'
        count = 0
        for item, qt in agent_entity.inventory.items():
            if item == "oak_log":
                self.inventory_str += (
                    '"'
                    + str(count)
                    + '":{"item":"'
                    + self.state.nameConversion(item)
                    + '","count":'
                    + str(qt)
                    + ',"damage":0,"maxdamage":0,"axis":"y","variant":"oak"}'
                )
            else:
                self.inventory_str += (
                    '"'
                    + str(count)
                    + '":{"item":"'
                    + self.state.nameConversion(item)
                    + '","count":'
                    + str(qt)
                    + ',"damage":0,"maxdamage":0}'
                )
            count += 1

        self.inventory_str += ","
        # prior to this, create a list of rooms and add the coords inside of each room to a certain index of the list (1, 2, 3...)
        # now, figure out what room the agent is currently in
        # when sensing the map, only sense blocks/entities that are in the same room as the agent
        currRoom = 0
        for index, room in enumerate(self.state.room_coords):
            if tuple(agent_entity.loc) in room:
                currRoom = index + 1

        self.entities_str = '"entities":{'

        self.e102loc = None
        e102 = self.state.get_entity_by_id(102)
        for index, room in enumerate(self.state.room_coords):
            if tuple(e102.loc) in room and tuple(agent_entity.loc) in room:
                self.e102loc = e102.loc
                self.entities_str += (
                    '"102":{"type":"EntityPogoist","name":"entity.polycraft.Pogoist.name","id":102,"pos":['
                    + str(72 + e102.loc[0])
                    + ",17,"
                    + str(64 + e102.loc[1])
                    + '],"color":"purple","equipment":[{"itemName":"Noble Pantoble","itemMeta":0,"count":1},{"itemName":"Noble Leggings","itemMeta":0,"count":1},{"itemName":"Noble Gorget","itemMeta":0,"count":1},{"itemName":"Noble Armet","itemMeta":0,"count":1}]},'
                )

        self.e103loc = None
        e103 = self.state.get_entity_by_id(103)
        for index, room in enumerate(self.state.room_coords):
            if tuple(e103.loc) in room and tuple(agent_entity.loc) in room:
                self.e103loc = e103.loc
                self.entities_str += (
                    '"103":{"type":"EntityTrader","name":"entity.polycraft.Trader.name",'
                    '"id":103,"pos":['
                    + str(72 + e103.loc[0])
                    + ",17,"
                    + str(64 + e103.loc[1])
                    + '],"color":"black","equipment":[{"itemName":"Sporty Nylon Stockings","itemMeta":0,"count":1},{"itemName":"Sporty Nylon Windbreaker","itemMeta":0,"count":1}]},'
                )

        self.e104loc = None
        e104 = self.state.get_entity_by_id(103)
        for index, room in enumerate(self.state.room_coords):
            if tuple(e104.loc) in room and tuple(agent_entity.loc) in room:
                self.e104loc = e104.loc
                self.entities_str += (
                    '"104":{"type":"EntityTrader","name":"entity.polycraft.Trader.name","id":104,"pos":['
                    + str(72 + e104.loc[0])
                    + ",17,"
                    + str(64 + e104.loc[1])
                    + '],"color":"black","equipment":[]},'
                )

        self.entities_str += "},"

        self.map_str = '"map":{'
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                for index, room in enumerate(self.state.room_coords):
                    if (i, j) in room and tuple(agent_entity.loc) in room:
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
        self.map_str += "}"
        self.state._step_count += 1
        self.result = "SUCCESS"
        self.action_metadata(agent_entity)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        print(
            'b{"blockInFront":{"name":"'
            + self.blockInFront
            + "},"
            + self.inventory_str
            + self.selected_item_str
            + '"player":{"pos":['
            + str(72 + agent_entity.loc[0])
            + ",17,"
            + str(64 + agent_entity.loc[1])
            + '],"facing":"'
            + agent_entity.facing
            + '","yaw":280.9509,"pitch":14.849994},"destinationPos":[0,0,0],'
            + self.entities_str
            + self.map_str
            + ', "size":[32,1,32],"origin":[72,17,64]},'
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
