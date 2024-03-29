from gym_novel_gridworlds2.object import Object, Entity
from typing import Union

class PolycraftObject(Object):
    placeable = True
    breakable = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in kwargs.items():
            if key == "breakable" or "_cost" in key:
                # set attr for all key
                setattr(self, key, val)
    
    def acted_upon(self, action_name, agent: Entity):
        # interact, break, use, etc
        if action_name == "break":
            self.state = "floating"

    @staticmethod
    def placement_reqs(map_state, loc):
        return False

    def get_symbol(self):
        """Gets text symbol for object"""
        return " "

    def get_img(self):
        """Gets image for object"""
        return None
