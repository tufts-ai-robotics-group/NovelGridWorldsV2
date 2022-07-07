from typing import List

from ..actions import Action, ActionSet

class Dynamic:
    def __init__(self, actions: List[Action], action_sets: List[ActionSet], action_space, obj_types):
        """
        actions: the instanciated classes and funcs that execute the actions
        action_sets: the set of action functions for each "set"
        action_space: open ai gym environment
        obj_types: classes for objects and types
        """
        self.actions = actions
        self.action_sets = action_sets
        self.action_space = action_space
        self.obj_types = obj_types
