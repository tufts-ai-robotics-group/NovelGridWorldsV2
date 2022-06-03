
class GenericAgent:
    def __init__(self, name, action_space, ob_space):
        self.name = name
        self.action_space = action_space
        self.ob_space = ob_space
    
    def get_action(self, observation):
        return self.action_space[0]


