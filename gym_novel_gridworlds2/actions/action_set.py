from typing import List, Tuple
from ..object.entity import Entity
from .action import Action 
from gym.spaces import Discrete

class ActionSet:
    def __init__(self, actions: List[Tuple[str, Action]]):
        self.actions = actions
    
    def do_action(self, entity, index):
        action: Action = self.actions[index]
        action.do_action(entity)

    def remove_action(self, index):
        pass

    def add_action(self, index):
        pass

    def get_action_names(self):
        return [a[0] for a in self.actions]

    def get_action_space(self):
        return Discrete(len(self.actions))
