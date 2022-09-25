from gym_novel_gridworlds2.object import Object


class PolycraftObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in kwargs.items():
            if "_cost" in key:
                # set attr for all key
                setattr(self, key, val)
    
    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"

    @staticmethod
    def placement_reqs(map_state, loc):
        return True
