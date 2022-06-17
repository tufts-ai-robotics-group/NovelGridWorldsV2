from .polycraft_obj import PolycraftObject

class Door(PolycraftObject):
    def __init__(self, typee, loc=(0, 0), state="block", **kwargs):
        self.type = typee
        self.loc = loc #update such that we update the 3D arr and add the item to it
        self.state = state #two states: block and floating
        self.isOpen = False
    
    def acted_upon(self, action_name, agent):
        if action_name = "use_door":
            if self.isOpen == True:
                self.isOpen = False
            else:
                self.isOpen = True
