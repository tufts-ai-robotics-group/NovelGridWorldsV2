from .agent import Agent

class RandomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def policy(self, observation):
        return self.get_action_space().sample()
