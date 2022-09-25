class Object:
    def __init__(self, type="unknown_type", loc=(0, 0), state="block", **kwargs):
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating

    def __str__(self):
        return f'<{self.__class__.__name__} "{str(self.type)}" at {str(self.loc)}>'

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        # there could be a broader "interact" action
        pass

    def walked_over(self):
        pass
