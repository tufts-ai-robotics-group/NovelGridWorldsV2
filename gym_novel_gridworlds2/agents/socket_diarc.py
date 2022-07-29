from ast import Mult
from typing import Optional
import numpy as np
from gym.spaces import Discrete, Dict, MultiDiscrete, Box
import json

from gym_novel_gridworlds2.state.dynamic import Dynamic

from .socket_agent import SocketManualAgent

def sense_all(state):
    pass

class SocketDiarcAgent(SocketManualAgent):
    def __init__(self, **kwargs):
        self.state_cache = None
        self.dynamics_cache: Optional[Dynamic] = None
        super.__init__(**kwargs)

    def get_observation_space(self, map_size: tuple, num_items: int, other_size: int):
        return Discrete(1) # dummy observation space to bypass sanity check
    
    def get_observation(self, state, dynamics):
        self.state_cache = state
        self.dynamics_cache = dynamics
        return super().get_observation()
    
    def policy(self, observation):
        # process the sense_all commands
        action = ""
        while not action.isdecimal():
            if action == "SENSE_ALL":
                self._send_msg(f">>>>>>>>> keyboard agent: Agent {self.name} can do these actions:")
            action_names = self.action_set.get_action_names()
            self._send_msg(">>>>>>>>>> " + ', '.join([f"{index}: {name}" for (index, name) in enumerate(action_names)]))
            action = self._recv_msg()
        return int(action)
    
    def update_metadata(self, metadata: dict):
        if type(metadata) == dict:
            msg = json.dumps(metadata)
        else:
            msg = metadata
        self._send_msg(json.dumps(msg))
