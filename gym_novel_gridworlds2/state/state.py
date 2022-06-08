from typing import List
from copy import deepcopy
import numpy as np
import random

from .entity_state import EntityState, Facing
from ..utils.item_encoder import SimpleItemEncoder


class State:
    def __init__(self, map_size: int, map_json=None, entities: List[str]=[], item_list={"air": 0}, **kwargs):
        self.initial_info = {
            "entities": entities,
            "map_size": map_size,
            "item_list": item_list,
            **kwargs
        }
        self.item_encoder = SimpleItemEncoder(item_list)

        if map_json is not None:
            self.load_map(map_json)

        # agents
        self._entity_states: List[EntityState] = {}
        for entity in entities:
            entity_id = self.item_encoder.get_id(entity)
            self._entity_states[entity_id] = EntityState()
        
        self._map = np.zeros(map_size)
        # self._world_inventory = {}
        self._step_count = 0

    
    def load_map(self, map_json):
        """
        Initializes the map, a 2D numpy array, using the provided JSON
        Initializes based off of selected mode 
        Randomization gets parameters from the JSON to initialize
        entities in random locations
        Seeded initializes entities in specified coords
        """
        self.mapper = dict()

        np.set_printoptions(threshold=np.inf)
        self.map_obj = np.zeros((map_json["map"]["size"], map_json["map"]["size"]))
        currId = 1
        for item, qt in map_json["map"]["objects"].items():
            for i in range(0, qt):
                row = random.randrange(0, map_json["map"]["size"])
                col = random.randrange(0, map_json["map"]["size"])
                if self.map_obj[row][col] == 0:
                    self.map_obj[row][col] = currId
            self.mapper[item] = currId
            currId += 1
        print(self.map_obj)
        print(self.mapper)


    def make_copy(self):
        return deepcopy(self)

    
    def get_object_id(self, object_name: str):
        return self.item_encoder.get_id(object_name)
    

    #############################   entity    ##############################
    def update_entity_loc(self, entity_name: str, new_loc: tuple):
        """
        Updates the location of an agent.
        """
        # notes: this algorithm updates both the agent state and the state.
        assert entity_id >= 0 and entity_id < len(self._entity_states)

        if new_loc is not None:
            prev_loc = self._entity_states[entity_id].location
            self._map[prev_loc] = self.item_encoder.get_id("air")
            self._map[new_loc] = self.get_entity_object_id(entity_id)
            self._entity_states[entity_id].location = new_loc
    
    def update_entity_facing(self, entity_name: str, new_facing: Facing):
        """
        Updates the facing of an agent.
        """
        assert entity_id >= 0 and entity_id < len(self._entity_states)

        self._entity_states[entity_id].facing = new_facing


    def update_entity_inventory(self, entity_id: int, item_id: int, quantity: int):
        self._entity_states[entity_id].inventory[item_id] = quantity

    
    ############################# OTHER BLOCKS #############################
    def update_map_loc(self, loc: tuple, new_item_str):
        self._map[loc] = self.item_encoder.get_id(new_item_str)


    def reset(self):
        self.__init__(*self.initial_info)
