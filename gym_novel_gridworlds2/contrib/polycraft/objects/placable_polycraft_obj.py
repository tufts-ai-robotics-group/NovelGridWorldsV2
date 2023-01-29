from .polycraft_obj import PolycraftObject


class PlacablePolycraftObject(PolycraftObject):
    @staticmethod
    def placement_reqs(map_state, loc):
        return True
