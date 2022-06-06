from typing import Tuple
import numpy as np
from .agent_state import AgentState
from copy import deepcopy

class State:
    def __init__(self, **kwargs):
        assert "agent_count" in kwargs
        assert "map_size" in kwargs

        self.agent_count = kwargs["agent_count"]
        self.map_size = kwargs["map_size"]
        self.initial_args = kwargs

        # agents
        self.agents = []
        for i in range(self.agent_count):
            self.agents.append(AgentState())
        
        self.map = np.zeros(self.map_size)
        self.world_inventory = {}
        self.step_count = 0
    

    def make_copy(self):
        return deepcopy(self)
    
    def reset(self):
        self.__init__(*self.initial_args)
