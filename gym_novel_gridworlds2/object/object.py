class Object:
    def __init__(self, typee, loc=(0, 0), state="block", **kwargs):
        self.type = typee
        self.loc = loc #update such that we update the 3D arr and add the item to it
        self.state = state #two states: block and floating
    
    def __str__(self):
        return f"<{self.__class__.__name__} at {str(self.loc)}>"

    def acted_upon(self, action_id, action_params):
        #there could be a broader "interact" action
        pass

    def walked_over(self):
        pass
