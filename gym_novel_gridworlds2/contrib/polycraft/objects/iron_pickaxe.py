from .polycraft_obj import PolycraftObject


class IronPickaxe(PolycraftObject):
    def __init__(self, type="iron_pickaxe", loc=(0, 0), state="floating", **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"
