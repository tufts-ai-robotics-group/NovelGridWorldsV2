from .object import Object


class Entity(Object):
    def __init__(
        self,
        type=None,
        loc=(0, 0),
        state="block",
        inventory={},
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

    def __str__(self):
        return f'<{self.__class__.__name__} "{str(self.type)}" facing {self.facing} at {str(self.loc)}>'

    def do_action(self, **kwargs):
        pass
