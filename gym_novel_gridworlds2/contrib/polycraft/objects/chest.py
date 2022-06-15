from .polycraft_obj import PolycraftObject

class Chest(PolycraftObject):
    def __init__(self, typee, loc=(0, 0), state="block", inventory=None, **kwargs):
        if inventory is None:
            inventory = []
        self.type = typee
        self.loc = loc #update such that we update the 3D arr and add the item to it
        self.state = state #two states: block and floating
        self.inventory = inventory
    
    def acted_upon(self, action_id, action_params):
        """
        TODO
        """
        return super().acted_upon(action_id, action_params)