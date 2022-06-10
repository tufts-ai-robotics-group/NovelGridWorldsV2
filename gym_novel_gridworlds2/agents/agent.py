
class GenericAgent:
    def __init__(self, name, action_space, ob_space):
        self.name = name
        self.action_space = action_space
        self.ob_space = ob_space
    
    def get_action(self, observation):
        raise NotImplementedError("Get action for " + self.name + " is not implemented.")
