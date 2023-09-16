from .placable_polycraft_obj import PlacablePolycraftObject


class BreakablePolycraftObject(PlacablePolycraftObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.breakable = True

