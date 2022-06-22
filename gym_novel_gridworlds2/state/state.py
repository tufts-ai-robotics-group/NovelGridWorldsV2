from typing import List, Optional, Tuple, Mapping
from copy import deepcopy
import numpy as np
import random
from functools import reduce
import json

from ..object import Object, Entity
from ..utils.item_encoder import SimpleItemEncoder
from .cell import Cell

AIR_STR = "air"

class LocationOutOfBound(IndexError):
    pass

class LocationOccupied(Exception):
    pass

class State:
    def __init__(self, map_size: Tuple[int]=None, \
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
            if objects is None:
                objects = map_json.get('objects')


        # TODO update
        self.initial_info = {
            "map_size": map_size,
            "objects": objects,
            "item_list": item_list,
            **kwargs
        }
        self.item_encoder = SimpleItemEncoder(item_list)

        # Initialization of the objects
        self._objects: Mapping[str, List[Object]] = {}
        self._map: np.ndarray = np.empty(map_size, dtype="object")
        self._map.fill(None)


        # for name, obj in objects.items():
        #     object_id = self.item_encoder.get_create_id(name)
        #     self.place_object(name, Object, properties=obj)
        
        # self._world_inventory = {}
        self._step_count = 0

    def make_copy(self):
        return deepcopy(self)


    def get_object_id(self, object_name: str):
        return self.item_encoder.get_create_id(object_name)
    

    def _ensure_not_none(self, loc: tuple):
        if self._map[loc] is None:
            self._map[loc] = Cell()


    ############################# ALL BLOCKS #############################
    def place_object(self, object_type: str, ObjectClass=Object, properties: dict = {}):
        """
        Places an object onto the map. 
        Returns true if success, false if there was a block there
        """
        # get the object id for use in the object dict
        object_id = self.item_encoder.get_create_id(object_type)

        # sanity check
        try:
            new_loc_obj = self._map[properties["loc"]]
        except IndexError as e:
            raise LocationOutOfBound from e
        
        # ensure there's a cell at this location
        self._ensure_not_none(properties["loc"])
        cell: Cell = self._map[properties["loc"]]

        # instanciate object
        obj = ObjectClass(object_type, **properties)

        # placing object in the map
        success = cell.place_object(obj)
        if not success:
            # map is full, skip the next step and raise an exception.
            raise LocationOccupied

        # placing object in the list
        if object_id not in self._objects:
            self._objects[object_id] = []
        self._objects[object_id].append(obj)

        return obj


    def random_place(self, object_str, count):
        """
        TODO: ObjectClass
        Randomly place the object in the map
        
        if there's not enough spots available, all available spots will be filled
        """
        all_available_spots = np.argwhere(self._map == None)
        if count >= all_available_spots.shape[0]:
            count = all_available_spots.shape[0]

        picked_indices = np.random.choice(a=all_available_spots.shape[0], size=count, replace=False)
        for index in picked_indices:
            properties = {"loc": tuple(all_available_spots[index])}
            # print(properties)
            self.place_object(object_str, properties=properties)

    
    def remove_object(self, object_name: str, loc: tuple):
        """
        Removes an object from the map, replacing it with air
        """

        # get the object id for use in the object dict
        object_id = self.item_encoder.get_id(object_name)
        if object_id is not None:
            # assert object_name in self._objects, f"Object {object_name} unknown."
            # won't work as object_name isnt directly comparable to objs
            # assert all(i >= j for i, j in zip(loc, [0] * self._map.ndim)), f"Location "
            obj = None  

            try:
                # find the location of the object.
                obj_index = next(i for i, v in enumerate(self._objects[object_id]) if v.loc == loc)
                obj = self._objects[object_id][obj_index]

                # remove the object from the list but without freeing.
                self._objects[object_id].pop(obj_index)

            except StopIteration:
                raise ValueError("Object " + object_name + \
                    " at " + str(loc) + " is not found in the list")
            
            # update the map
            cell: Cell = self._map[loc]
            cell.remove_object(obj)
    

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


    def get_objects_at(self, loc: tuple):
        """
        Gets all objects at a specific location.
        """
        if self._map[loc] is None:
            return ([], [])
        else:
            return self._map[loc].get_obj_entities()
    
    def get_object_at(self, loc: tuple):
        """
        LEGACY API:
        Gets an object at a specific location.
            If there are multiple objects, the first non-entity 
            object will be returned.
        Returns None if it's not found.

        WARNING: Do not modify the locations
        """
        if self._map[loc] is None:
            return None
        objs = self._map[loc].get_obj_entities()
        if len(objs[0]) > 0:
            return objs[0][0]
        elif len(objs[1]) > 0:
            return objs[1][0]
        return None


    def update_object_loc(self, old_loc: tuple, new_loc: tuple):
        """
        Updates the location of an object.
        """
        # notes: this algorithm updates both the agent state and the state.

        #does this not handle cases where an object is already there?

        if self.get_object_at(new_loc) == None:
            obj = self.get_object_at(old_loc)
            self._map[old_loc].remove_object(obj)

            self._ensure_not_none(new_loc)
            self._map[new_loc].place_object(obj)
            obj.loc = new_loc
            return True
        else:
            return False
    
    def is_full(self, loc: tuple):
        if self._map[loc] is None:
            return (False, False)
        return self._map[loc].is_full()
    
    def contains_block(self, loc: tuple):
        if self._map[loc] is None:
            return False
        return self._map[loc]._contains_block

    # def get_object_state(self, loc: tuple):
    #     """
    #     Gets the state of an object at a specific location
    #     """
    #     obj = self.get_object_at(loc)
    #     return obj.state

    # def update_object_state(self, loc: tuple):
    #     """
    #     Updates state of an object at a specific location
    #     If it was a block, it is now floating, and vice versa
    #     """
    #     obj = self.get_object_at(loc)
    #     if obj.state == "block":
    #         obj.state = "floating"
    #     else:
    #         obj.state = "block"

    def clear(self):
        """
        Removes all objects from the list and clears the map/item list
        TODO not tested
        """
        #remove all objects:
        for index, obj_id in np.ndenumerate(self._map):
            if obj_id is not None:
                obj = self.get_object_at(index)
                print(obj)
                # print(obj.type, index)
                if obj is not None:
                    self.remove_object(obj.type, index)
        #resets item encoder
        self.item_encoder = SimpleItemEncoder()
        #old version:
        """
        TODO: UNUSABLE FOR NOW, UPDATE NEEDED
        """
        # self.__init__(*self.initial_info)