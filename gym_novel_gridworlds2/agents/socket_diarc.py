from ast import Mult
from typing import Optional
import numpy as np
from gymnasium import spaces
import json
from gym_novel_gridworlds2.actions.action_set import CommandParseError

from gym_novel_gridworlds2.state.dynamic import Dynamic

from .socket_agent import SocketManualAgent

PARAMETER_MIN = -10000
PARAMETER_MAX =  10000

def sense_all(state):
    pass

class SocketDiarcAgent(SocketManualAgent):
    def __init__(self, **kwargs):
        self.state_cache = None
        self.dynamics_cache: Optional[Dynamic] = None
        super().__init__(**kwargs)

    def get_observation_space(self, map_size: tuple, other_size: int):
        return spaces.Discrete(1) # dummy observation space to bypass sanity check

    def get_observation(self, state, dynamics):
        self.state_cache = state
        self.dynamics_cache = dynamics
        return super().get_observation(state, dynamics)

    def get_action_space(self):
        # uses an extra tuple for parameters
        return self.action_set.get_action_space()
    
    def policy(self, observation):
        # process the sense_all commands
        while True:
            action = self._recv_msg()
            try:
                command = self.action_set.parse_command(action)
                return command
            except CommandParseError:
                self._send_msg(json.dumps({
                    "goal":{
                        "goalType":"ITEM",
                        "goalAchieved":False,
                        "Distribution":"Uninformed"
                    }, 
                    "command_result":{
                        "command":"WRONG_CMD",
                        "argument":"",
                        "result":"FAIL",
                        "message":"Invalid Command",
                        "stepCost":0.0
                    },
                    "step":0,
                    "gameOver":False
                }))
    
    def update_metadata(self, metadata: dict):
        if type(metadata) == str:
            msg = json.dumps(metadata + "\n")
        else:
            msg = json.dumps(metadata)
        
        self._send_msg(msg)
