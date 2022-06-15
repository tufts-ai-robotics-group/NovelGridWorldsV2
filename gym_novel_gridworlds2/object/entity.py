from .object import Object
from enum import Enum

class Facing(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Entity(Object):
    def __init__(self, name="", loc=(0, 0), type=None, inventory={}, facing="NORTH"):
        # convert to enum
        facing = Facing[facing]

        # populate
        self.name = name
        self.loc = loc
        self.inventory = inventory
        self.type = type
        self.facing = facing


    def do_action(self):
        pass
