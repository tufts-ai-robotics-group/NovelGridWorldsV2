from typing import List, Optional, Tuple, Mapping
from copy import deepcopy
from matplotlib.style import available
import numpy as np
import random
from functools import reduce
import json

from ..object import Object, Entity
from ..utils.item_encoder import SimpleItemEncoder

AIR_STR = "air"

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
        self._map = np.zeros((map_size[0], map_size[1], 1)) #3D array
        # self._map = np.zeros(map_size)

        # for name, obj in objects.items():
        #     object_id = self.item_encoder.get_create_id(name)
        #     self.place_object(name, Object, properties=obj)
        
        # self._world_inventory = {}
        self._step_count = 0

    def make_copy(self):
        return deepcopy(self)


    def get_object_id(self, object_name: str):
        return self.item_encoder.get_create_id(object_name)

    def new3DSpot(self, object_id, loc):
        """
        At a specified location, expands 3D array to place the new 
        id there
        """
        arr = self._map[loc]
        np.append(arr, object_id)
        self._map[loc] = arr

    ############################# ALL BLOCKS #############################
    def place_object(self, object_type: str, ObjectClass=Object, properties: dict = {}):
        """
        Places an object onto the map. 
        Returns true if nothing or floating obj there, false if there was a block
        """
        # get the object id for use in the object dict
        object_id = self.item_encoder.get_create_id(object_type)
        self._objects[object_id] = []

        # if self._map[properties["loc"]] != 0: #case where an item is already there
        #     return False

        there = self._map[properties["loc"]]

        if len(there) == 1: #one item, could be block
            # obj = self._map[properties["loc"][0], properties["loc"][1], 0]
            obj = self.get_objects_at(properties["loc"])
            # print(obj)
            if obj is not None:
                if obj[0].state == "block": #there is a block here, can't place 
                    return False
                else: #there is a floating obj here, can place if also floating obj
                    if properties["state"] == "floating":
                        new3DSpot(object_id, properties["loc"])
                    else:
                        return False
            else: #just air, update to object
                # print("look at me")
                self._map[properties["loc"][0], properties["loc"][1], 0] = object_id
        else: #multiple items, has to be floating
            if object_id not in self._objects:
                if properties["state"] == "floating":
                    new3DSpot(object_id, properties["loc"])
                else:
                    return False    
            
        # self._map[properties["loc"]] = object_id
        # self._objects[object_id].append(ObjectClass(object_type, **properties))
        self._objects[object_id].append(ObjectClass(object_type, properties["loc"], properties["state"]))

        return True

    def random_place(self, object_str, count):
        """
        TODO: ObjectClass
        Randomly place the object in the map
        
        if there's not enough spots available, all available spots will be filled
        """
        all_available_spots = np.argwhere(self._map == 0)
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


    def get_objects_at(self, loc: tuple):
        """
        Gets a specific object at a specific location.
        Returns None if it's not found.
        WARNINGL Do not modify the locations
        """
        to_return = []
        print(self._map[loc])
        for i in range(len(self._map[loc])):
            print("i:", i)
            obj_type = self._map[loc[0], loc[1], i]
            print("type:", obj_type)
            #error: recognizes obj as none
            print([self._objects.get(obj_type)])
            for obj in self._objects.get(obj_type) or []:
                if obj.loc == loc:
                    np.append(to_return, obj)
        if len(to_return) == 0:
            return None
        else:
            return to_return

        """
        obj_type = self._map[loc][0]
        for obj in self._objects.get(obj_type) or []:
            if obj.loc == loc:
                if len(self._map[loc]) > 1:
                    #get all the other objects at this location
                    return [obj]
                else:
                    return obj
        return None
        """
    """
    def get_object_at(self, loc: tuple):
        
        Gets a specific object at a specific location.
        Returns None if it's not found.
        WARNINGL Do not modify the locations
        
        obj_type = self._map[loc]
        for obj in self._objects.get(obj_type) or []:
            if obj.loc == loc:
                return obj
        return None
    """
    

    def update_object_loc(self, old_loc: tuple, new_loc: tuple):
        """
        Updates the location of an object.
        """
        # notes: this algorithm updates both the agent state and the state.

        #does this not handle cases where an object is already there?

        if self.get_object_at(new_loc) == None:
            obj = self.get_object_at(old_loc)
            self._map[old_loc] = self.item_encoder.get_create_id("air")
            self._map[new_loc] = self.item_encoder.get_create_id(obj.type)
            obj.loc = new_loc
            return True
        else:
            return False

    def get_object_state(self, loc: tuple):
        """
        Gets the state of an object at a specific location
        """
        obj = self.get_object_at(loc)
        return obj.state

    def update_object_state(self, loc: tuple):
        """
        Updates state of an object at a specific location
        If it was a block, it is now floating, and vice versa
        """
        obj = self.get_object_at(loc)
        if obj.state == "block":
            obj.state = "floating"
        else:
            obj.state = "block"


    def reset(self):
        """
        Removes all objects from the list and clears the map/item list
        """
        #remove all objects:
        for index, obj_id in np.ndenumerate(self._map):
            if obj_id != 0:
                obj = self.get_object_at(index)
                print(obj.type, index)
                self.remove_object(obj.type, index)
        #resets item encoder
        self.item_encoder = SimpleItemEncoder()
        #old version:
        """
        TODO: UNUSABLE FOR NOW, UPDATE NEEDED
        """
        # self.__init__(*self.initial_info)