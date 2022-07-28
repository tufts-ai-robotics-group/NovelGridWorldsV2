from .agent import Agent


class NOPAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def policy(self, observation):
        action_sets = self.action_set.get_action_names()
        return action_sets.index("NOP")

    def get_observation(self):
        return []
