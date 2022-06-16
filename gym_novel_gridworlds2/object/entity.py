from .object import Object

class Entity(Object):
    def __init__(self, name="", loc=(0, 0), type=None, inventory={}, facing="NORTH"):

        # populate
        self.name = name
        self.loc = loc
        self.inventory = inventory
        self.type = type
        self.facing = facing

    
    def __str__(self):
        return f"<{self.__class__.__name__} \"{str(self.type)}\" facing {self.facing} at {str(self.loc)}>"


    def do_action(self):
        pass
