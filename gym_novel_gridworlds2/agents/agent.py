from gym import Space
from gym.spaces import Discrete

from gym_novel_gridworlds2.actions.action import Action

from ..actions.action_set import ActionSet


class Agent:
    def __init__(
        self,
        id: int,
        action_set: ActionSet,
        state,
        entity_data,
        ob_space: Space = None, 
        **kwargs
    ):
        self.id = id
        self.action_set = action_set
        self.state = state
        self.entity_data = entity_data
        self.ob_space = ob_space

    ### Socket related functions
    def is_ready(self):
        return True

    def generate_observation(self, state):
        return [0]

    def get_observation_space(self, map_size: tuple, other_size: int):
        return Discrete(1)
    
    def get_observation(self, state, dynamic):
        # raise NotImplementedError("Get observation for " + self.name + " is not implemented.")
        return []
    
    def get_action_space(self):
        return self.action_set.get_action_space()
    
    def update_metadata(self, metadata: dict):
        pass
    
    def policy(self, observation):
        """
        Main policy for the agent
        """
        raise NotImplementedError(
            "Get action for " + self.id + " is not implemented."
        )
