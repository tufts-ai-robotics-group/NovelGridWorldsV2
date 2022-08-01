# from scipy.fft import idct
from .object import Object


class Entity(Object):
    def __init__(
        self,
        type=None,
        loc=(0, 0),
        state="block",
        inventory={},
        id=1,
        name="",
        facing="NORTH",
        **kwargs,
    ):

        # populate
        self.name = name
        self.loc = loc
        self.inventory = inventory
        self.selectedItem: str = None
        self.type = type
        self.facing = facing
        self.state = state
        self.id = id

    def __str__(self):
        return f'<{self.__class__.__name__} "{str(self.type)}" ({self.id}) facing {self.facing} at {str(self.loc)}>'

    def do_action(self, **kwargs):
        pass
