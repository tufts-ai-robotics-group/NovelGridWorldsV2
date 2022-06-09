from typing import List, Optional, Tuple, Mapping
from copy import deepcopy
import numpy as np
import random
from functools import reduce

from ..object import Object, Entity
from ..utils.item_encoder import SimpleItemEncoder

AIR_STR = "air"

class State:
    def __init__(self, map_size: Tuple[int]=None, \
            entities: Optional[Mapping[str, object]]=None, \
            objects: Mapping[str, object]=None,
            map_json: dict=None, \
            item_list: Mapping[str, int]={"air": 0}, \
            **kwargs):
        """
        Initialization of the State Object.
        """
        if map_json is not None:
            if map_size is None:
                map_size = tuple(map_json.get('map').get('size'))
            if entities is None:
                entities = map_json.get('entities')
            if objects is None:
                objects = map_json.get('objects')


        # TODO update
        self.initial_info = {
            "entities": entities,
            "map_size": map_size,
            "objects": objects,
            "item_list": item_list,
            **kwargs
        }
        self.item_encoder = SimpleItemEncoder(item_list)

        # Initialization of the objects
        self._objects: Mapping[str, List[Object]] = {}
        for name, object in objects.items():
            object_id = self.item_encoder.get_create_id(name)
            self._objects[object_id] = Object(name=name, **object)

        for name, entity in entities.items():
            entity_id = self.item_encoder.get_create_id(name)
            self._objects[entity_id] = Entity(name=name, **entity)

        self._map = np.zeros(map_size)
        # self._world_inventory = {}
        self._step_count = 0


    def random_place(self, object_str, count):
        """
        TODO
        Randomly place the object in the map
        """
        for i in range(0, count):
            row = random.randrange(0, self.map_size[0])
            col = random.randrange(0, self.map_size[1])
            object_str.loc = [row, col]
            print(object_str.loc)
            if not place_object(object_str):
                i -= 1

    def make_copy(self):
        return deepcopy(self)


    def get_object_id(self, object_name: str):
        return self.item_encoder.get_create_id(object_name)


    ############################# ALL BLOCKS #############################
    def place_object(self, object_name: str, type=Object, properties: dict = {}):
        """
        Places an object onto the map. 
        Unchecked error if there's existing at the location.
        """
        # get the object id for use in the object dict
        object_id = self.item_encoder.get_id(object_name)

        if object_name not in self._objects:
            self._objects[object_name] = []

        if self._map[properties["loc"]] != 0:
            return False
        
        self._map[properties["loc"]] = self.item_encoder.get_create_id(object_id)
        self._objects[object_id].append(Object(object_name, **properties))

        return True


    
    def remove_object(self, object_name: str, loc: tuple):
        """
        Removes an object from the map, replacing it with air
        """
        assert object_name in self._objects, f"Object {object_name} unknown."
        # assert all(i >= j for i, j in zip(loc, [0] * self._map.ndim)), f"Location "

        # get the object id for use in the object dict
        object_id = self.item_encoder.get_id(object_name)

        # update the map
        self._map[loc] = self.item_encoder.get_create_id(AIR_STR)

        try:
            # find the location of the object.
            obj_index = next(i for i, v in enumerate(self._objects[object_id]) if v.loc == loc)

            # remove the object from the list but without freeing.
            self._objects[object_id].pop(obj_index)
        except StopIteration:
            raise ValueError("Object " + object_name + \
                " at " + str(loc) + " is not found in the list")
    

    def get_objects_of_type(self, object_type: str):
        """
        Gets a list of objects of specific type
        WARNING: Do not modify the locations in the object!!
        """
        type_id = self.item_encoder.get_id(object_type)
        if type_id is not None:
            return self._objects.get(type_id) or []
        else:
            return []


    def get_object_at(self, loc: tuple):
        """
        Gets a specific object at a specific location
        WARNINGL Do not modify the locations
        """
        pass

    

    def update_object_loc(self, entity_name: str, new_loc: tuple):
        """
        TODO
        Updates the location of an agent.
        """
        # notes: this algorithm updates both the agent state and the state.
        assert entity_name in self.item_encoder.item_dict

        if new_loc is not None:
            prev_loc = self._entity_states[entity_id].location
            self._map[prev_loc] = self.item_encoder.get_create_id("air")
            self._map[new_loc] = self.get_entity_object_id(entity_id)
            self._entity_states[entity_id].location = new_loc


    def reset(self):
        self.__init__(*self.initial_info)
