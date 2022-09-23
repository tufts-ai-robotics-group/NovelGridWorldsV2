from .polycraft_obj import PolycraftObject


class Door(PolycraftObject):
    def __init__(self, type="door", loc=(0, 0), state="block", facing="NORTH", **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating
        self.canWalkOver = False
        self.open = False
        self.facing = facing

    @staticmethod
    def placement_reqs(map_state, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "use":
            if self.canWalkOver == True:
                self.canWalkOver = False
                self.open = False
            else:
                self.canWalkOver = True
                self.open = True
        elif action_name == "break":
            self.state = "floating"
