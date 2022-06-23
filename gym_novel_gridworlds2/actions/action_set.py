from ..object.entity import Entity
from .action import Action 
from gym.spaces import Discrete

class ActionSet:
    def __init__(self, actions: Action, entity: Entity):
        self.actions = actions
        self.entity = entity
    
    def do_action(self, index):
        action: Action = self.actions[index]
        action.do_action(self.entity)

    def remove_action(self, index):
        pass

    def add_action(self, index):
        pass

    def get_actionset(self):
        return Discrete(len(self.actions))
