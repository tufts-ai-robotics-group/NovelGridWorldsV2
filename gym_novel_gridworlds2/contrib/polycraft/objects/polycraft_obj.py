from gym_novel_gridworlds2.object import Object


class PolycraftObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "break_cost" in kwargs:
            self.break_cost = kwargs["break_cost"]
            del kwargs["break_cost"]
    
    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"

    def placement_reqs(self, map_state, loc):
        return True
