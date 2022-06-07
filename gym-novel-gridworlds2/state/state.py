from typing import List
from copy import deepcopy
import numpy as np

from .entity_state import EntityState, Facing
from ..utils.item_encoder import SimpleItemEncoder


class State:
    def __init__(self, agent_count, map_size, item_list=["air"], **kwargs):
        self.initial_info = {
            "agent_count": agent_count,
            "map_size": map_size,
            "item_list": item_list
            **kwargs
        }
        self.item_encoder = SimpleItemEncoder(item_list)

        # agents
        self._entity_states: List[EntityState] = []
        for _ in range(agent_count):
            self._entity_states.append(EntityState())
        
        self._map = np.zeros(map_size)
        self._world_inventory = {}
        self._step_count = 0
    

    def make_copy(self):
        return deepcopy(self)
    

    #############################   entity    ##############################
    def update_entity_loc(self, entity_id, new_facing=None, new_loc=None):
        """
        Updates the location of an agent.
        """
        # notes: this algorithm updates both the agent state and the state.
        assert entity_id >= 0 and entity_id < len(self._entity_states)

        if new_loc is not None:
            prev_loc = self._entity_states[entity_id].location
            self._map[prev_loc] = self.item_encoder.get_id("air")
            self._map[new_loc] = self.item_encoder.get_id("entity-" + str(entity_id))
            self._entity_states[entity_id].location = new_loc
    
    def update_entity_facing(self, entity_id: int, new_facing: Facing):
        """
        Updates the facing of an agent.
        """
        assert entity_id >= 0 and entity_id < len(self._entity_states)

        self._entity_states[entity_id].facing = new_facing


    def update_entity_inventory(self, entity_id, item_id, quantity):
        self._entity_states[entity_id].inventory[item_id] = quantity

    
    ############################# OTHER BLOCKS #############################
    def update_map_loc(self, loc: tuple, new_item_str):
        pass


    def reset(self):
        self.__init__(*self.initial_info)
