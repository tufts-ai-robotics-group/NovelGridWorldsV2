from .agent import Agent

class RandomAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def policy(self, observation):
        return self.get_action_space().sample()
