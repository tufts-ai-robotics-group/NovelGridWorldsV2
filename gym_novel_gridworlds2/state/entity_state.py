class EntityState:
    def __init__(self, facing="NORTH", location=(0, 0), \
                inventory={}, last_action="", last_action_cost=0):
        self.facing = facing
        self.location = location
        self.inventory = inventory
