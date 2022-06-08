from enum import Enum

class Facing(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class EntityState:
    def __init__(self, facing=Facing.NORTH, location=(0, 0), \
                inventory={}, last_action="", last_action_cost=0):
        self.facing = facing
        self.location = location
        self.inventory = inventory
