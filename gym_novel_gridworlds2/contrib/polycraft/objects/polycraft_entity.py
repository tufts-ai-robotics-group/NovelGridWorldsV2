
from .polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.object.entity import Entity


class PolycraftEntity(PolycraftObject, Entity):
    entity_type = None
    
    def print_agent_status(self):
        print("     inventory:", self.inventory)
