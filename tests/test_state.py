import unittest
import numpy as np 
import json

from gym_novel_gridworlds2.state import State

class StateTestPlacement(unittest.TestCase):
    def testPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc], obj_type_id)
        self.assertEqual(len(state._objects[obj_type_id]), 1)
    
    def testPlaceItemOverItem(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        state.place_object("tree", properties={"loc": loc})
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc], obj_type_id)
        self.assertEqual(len(state._objects[obj_type_id]), 1)
    
    def testPlaceItemOverItem2(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        state.place_object("chest", properties={"loc": loc})
        obj_type_id_1 = state.item_encoder.get_id("tree")
        obj_type_id_2 = state.item_encoder.get_id("chest")
        self.assertEqual(state._map[loc], obj_type_id_1)
        self.assertEqual(len(state._objects[obj_type_id_1]), 1)
        self.assertTrue(obj_type_id_2 not in state._objects)

    
    def testrandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=2)
        self.assertEqual((state._map == 1).sum(), 2)
        self.assertEqual(len(state._objects[1]), 2)


    def testrandomPlaceItemFull(self):
        state = State(map_size=(2, 2), objects=[])
        state.random_place(object_str="tree", count=5)
        self.assertEqual((state._map == 1).sum(), 4)
        self.assertEqual(len(state._objects[1]), 4)



# class StateTestChangeMap(unittest.TestCase):
#     def setUp(self):
#         self.state = State(entity_count=1, map_size=(10,10))

#     def testChangeAgentLoc(self):
#         self.state.update_map_loc((3, 5), "entity-1")
#         self.assertEqual(self.state._map[3, 5], 1)


# class StateTestChangeEntityLoc(unittest.TestCase):
#     def setUp(self):
#         self.state = State(entity_count=1, map_size=(10,10))
#         print(self.state.item_encoder.item_dict)

#     def testChangeAgentLoc(self):
#         entity_id = 0
#         new_loc = (3, 5)

#         old_loc = self.state._entity_states[0].location
#         self.state.update_entity_loc(entity_id, new_loc)
#         entity_id_str_encoded = self.state.item_encoder.get_create_id("entity-" + str(entity_id))

#         self.assertEqual(self.state._map[new_loc], entity_id_str_encoded)
#         self.assertEqual(self.state._map[old_loc], self.state.item_encoder.get_create_id("air"))
#         self.assertEqual(self.state._entity_states[0].location, new_loc)

