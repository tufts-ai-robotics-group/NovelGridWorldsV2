from typing import List, Tuple

from numpy import object_
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
        self._contains_block = False
    
    def place_object(self, obj: Entity) -> bool:
        """
        If the number of entities is within the limit, place the object and return true.
        Otherwise, return false and do nothing.
        """
        is_full = self.is_full()
        if isinstance(obj, Entity) and not is_full[1]:
            self._entities.append(obj)
            return True
        elif isinstance(obj, Object) and not is_full[0]:
            self._objects.append(obj)
            if obj.state == "block":
                self._contains_block = True
            return True
        return False
    

    def is_full(self):
        """
        returns whether the cell is full or not.
        (enti)
        """
        if self._contains_block:
            return (True, True)
        return (len(self._objects) >= self._obj_limit, len(self._entities) >= self._entity_limit)


    def remove_object(self, obj: Object):
        """
        Removes an object from the cell.
        raises Value Error if the item does not exist
        """
        if isinstance(obj, Entity):
            self._entities.remove(obj)
        else:
            self._objects.remove(obj)
            if obj.state == "block":
                self._contains_block = False

    def clear(self):
        """
        clears everything in the cell.
        """
        self._objects = []
        self._entities = []


    def get_obj_entities(self) -> Tuple[List[Object], List[Entity]]:
        return (self._objects, self._entities)
