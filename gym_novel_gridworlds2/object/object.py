class Object:
    def __init__(self, type, loc=[0, 0], **kwargs):
        self.type = type
        self.loc = loc
    
    def __str__(self):
        return f"<{self.__class__.__name__} at {str(self.loc)}>"

    def acted_upon(self, action_id, action_params):
        #there could be a broader "interact" action
        pass

    def walked_over(self):
        pass
