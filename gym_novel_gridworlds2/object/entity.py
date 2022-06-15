from .object import Object

class Entity(Object):
    def __init__(self, name="", loc=(0, 0), type=None, inventory={}, facing="NORTH"):

        # populate
        self.name = name
        self.loc = loc
        self.inventory = inventory
        self.type = type
        self.facing = facing


    def do_action(self):
        pass
