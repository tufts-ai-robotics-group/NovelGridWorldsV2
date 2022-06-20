from typing import List, Tuple
from gym_novel_gridworlds2.object import Object, Entity

class Cell:
    """
    Cell class, representing a grid box of the grid world
    when updating the obj/entities, use the functions. 
    when getting the obj/entities, just directly access this,
    """
    def __init__(self, obj_limit=1, entity_limit=1, item_encoder=None):
        self._objects = []
        self._entities = []
        self._obj_limit = obj_limit
        self._entity_limit = entity_limit
        self._item_encoder = item_encoder
    
    def place_object(self, obj: Object) -> bool:
        """
        If the number of objects is within the limit, place the object and return true.
        Otherwise, return false and do nothing.
        """
        if len(self._objects) < self._obj_limit:
            self._objects.append(obj)
            return True
        else:
            return False
    
    def place_entity(self, entity: Entity) -> bool:
        """
        If the number of entities is within the limit, place the object and return true.
        Otherwise, return false and do nothing.
        """
        if len(self._entities) < self._entity_limit:
            self._objects.append(entity)
            return True
        else:
            return False
    
    def remove_object(self, obj: Object):
        self._objects.remove(obj)
    
    def remove_entity(self, entity: Entity):
        self._entities.remove(entity)
    
    def clear(self):
        self._objects = []

    def get_obj_entities(self) -> Tuple[List[Object], List[Entity]]:
        return (self._objects, self._entities)
