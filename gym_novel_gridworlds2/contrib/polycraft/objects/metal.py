from .polycraft_obj import PolycraftObject


class Metal(PolycraftObject):
    def __init__(self, type="metal_obj", loc=(0, 0), state="block", **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        

    def placement_reqs(self, map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            if agent.selectedItem == "iron_pickaxe":
                self.state = "floating"
