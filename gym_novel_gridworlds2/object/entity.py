# from scipy.fft import idct
from .object import Object


class Entity(Object):
    def __init__(
        self,
        type=None,
        loc=(0, 0),
        state="block",
        inventory=None, # bad idea to use this default here right? because its mutable. Use None and replace instead
        id=1,
        name="",
        nickname="",
        facing="NORTH",
        **kwargs,
    ):

        # populate
        self.name = name
        self.nickname = nickname
        self.loc = loc
        self.inventory = inventory if inventory is not None else {}
        self.selectedItem: str = None
        self.type = type
        self.facing = facing
        self.state = state
        self.id = id

    def __str__(self):
        return f'<{self.__class__.__name__} "{str(self.type)}" ({self.id}) facing {self.facing} at {str(self.loc)}>'

    def do_action(self, **kwargs):
        pass

    def add_to_inventory(self, item, amount):
        if item not in self.inventory:
            self.inventory[item] = amount
        else:
            self.inventory[item] += amount
    
    def print_agent_status(self):
        pass
