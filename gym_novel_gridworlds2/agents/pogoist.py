from .agent import Agent


class Pogoist(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isMoving = False

    def policy(self, observation):
        if self.isMoving:
            self.isMoving = False
            action_sets = self.action_set.get_action_names()
            to_do = self.get_action_space().sample()
            while to_do == action_sets.index("NOP"):
                to_do = self.get_action_space().sample()
            return to_do
        else:  # skip every other turn
            self.isMoving = True
            action_sets = self.action_set.get_action_names()
            return action_sets.index("NOP")

    def get_observation(self):
        return []
