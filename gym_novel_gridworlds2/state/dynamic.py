class Dynamic:
    def __init__(self, actions, action_sets, action_space, obj_types):
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
