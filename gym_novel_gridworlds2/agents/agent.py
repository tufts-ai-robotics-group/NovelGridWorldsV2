from gym import Space
from gym.spaces import Discrete

from gym_novel_gridworlds2.actions.action import Action

from ..actions.action_set import ActionSet

class Agent:
    def __init__(self, name: str, action_set: ActionSet, ob_space: Space=None):
        self.name = name
        self.action_set = action_set
        self.ob_space = ob_space
    
    def generate_observation(self, state):
        return []
    
    def get_observation_space(self, map_size: tuple, other_size: int):
        return Discrete(0)
    
    def get_observation(self):
        raise NotImplementedError("Get observation for " + self.name + " is not implemented.")
    
    def get_action_space(self):
        return self.action_set.get_action_space()
    
    def get_action(self, observation):
        raise NotImplementedError("Get action for " + self.name + " is not implemented.")
