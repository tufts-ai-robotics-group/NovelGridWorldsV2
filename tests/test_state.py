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

    def testPlaceTwoItems(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("chest", properties={"loc": loc2})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc1], obj_type_id1)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(state._map[loc2], obj_type_id2)
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

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

    def testDoubleRandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        self.assertEqual((state._map == 1).sum(), 3)
        self.assertEqual(len(state._objects[1]), 3)

        state.random_place(object_str="chest", count=1)
        self.assertEqual((state._map == 2).sum(), 1)
        self.assertEqual(len(state._objects[2]), 1)

    def testMultipleRandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        self.assertEqual((state._map == 1).sum(), 3)
        self.assertEqual(len(state._objects[1]), 3)

        state.random_place(object_str="chest", count=1)
        self.assertEqual((state._map == 2).sum(), 1)
        self.assertEqual(len(state._objects[2]), 1)

        state.random_place(object_str="crafting_table", count=1)
        self.assertEqual((state._map == 3).sum(), 1)
        self.assertEqual(len(state._objects[3]), 1)

        state.random_place(object_str="iron", count=2)
        self.assertEqual((state._map == 4).sum(), 2)
        self.assertEqual(len(state._objects[4]), 2)

    def testMultipleRandomPlaceItemFull(self):
        state = State(map_size=(2, 2), objects=[])
        state.random_place(object_str="tree", count=3)
        self.assertEqual((state._map == 1).sum(), 3)
        self.assertEqual(len(state._objects[1]), 3)

        state.random_place(object_str="chest", count=1)
        self.assertEqual((state._map == 2).sum(), 1)
        self.assertEqual(len(state._objects[2]), 1)

        state.random_place(object_str="crafting_table", count=1)
        self.assertEqual((state._map == 3).sum(), 0)

        state.random_place(object_str="iron", count=2)
        self.assertEqual((state._map == 4).sum(), 0)

    def testRemoveObject(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc1], obj_type_id1)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        state.remove_object("tree", loc1)
        self.assertEqual(state._map[loc1], 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 0)

    def testRemoveIllegalObject(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc1], obj_type_id1)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        state.remove_object("car", loc1)
        self.assertEqual(state._map[loc1], obj_type_id1)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

    # should fail:
    # def testRemoveWrongObject(self):
    #     state = State(map_size=(5, 5), objects=[])
    #     loc1 = (2, 3)
    #     loc2 = (3, 3)
    #     state.place_object("tree", properties={"loc": loc1})

    #     obj_type_id1 = state.item_encoder.get_id("tree")
    #     self.assertEqual(state._map[loc1], obj_type_id1)
    #     self.assertEqual(len(state._objects[obj_type_id1]), 1)

    #     state.remove_object("tree", loc2)
    #     self.assertEqual(state._map[loc1], 1)
    #     self.assertEqual(len(state._objects[obj_type_id1]), 1)

    def testRemoveOneWhenTwoObjects(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc2})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 2)

        state.remove_object("tree", loc2)
        self.assertEqual(state._map[loc1], 1)
        self.assertEqual(state._map[loc2], 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

    def testRemoveTwoObjects(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc2})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 2)

        state.remove_object("tree", loc2)
        self.assertEqual(state._map[loc1], 1)
        self.assertEqual(state._map[loc2], 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        state.remove_object("tree", loc1)
        self.assertEqual(state._map[loc1], 0)
        self.assertEqual(state._map[loc2], 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 0)

    def testGetObjectsRandom(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        self.assertEqual((state._map == 1).sum(), 3)
        self.assertEqual(len(state._objects[1]), 3)

        state.random_place(object_str="chest", count=1)
        self.assertEqual((state._map == 2).sum(), 1)
        self.assertEqual(len(state._objects[2]), 1)

        arr = state.get_objects_of_type("tree")
        print(arr[0].loc)
        print(arr[1].loc)
        print(arr[2].loc)
        self.assertEqual(len(arr), 3)

    def testGetObjectsDeterministic(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc2})

        obj_type_id1 = state.item_encoder.get_id("tree")

        arr = state.get_objects_of_type("tree")
        self.assertEqual(arr[0].loc, loc1)
        self.assertEqual(arr[1].loc, loc2)
        self.assertEqual(len(arr), 2)

    def testGetObjectAt1(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc2})

        obj1 = state.get_object_at(loc1)
        self.assertEqual(obj1.type, "tree")

        obj2 = state.get_object_at(loc2)
        self.assertEqual(obj2.type, "tree")

    def testGetObjectAt2(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("chest", properties={"loc": loc2})

        obj1 = state.get_object_at(loc1)
        self.assertEqual(obj1.type, "tree")

        obj2 = state.get_object_at(loc2)
        self.assertEqual(obj2.type, "chest")

    def testGetObjectAtNone(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 3)
        state.place_object("tree", properties={"loc": loc1})

        obj1 = state.get_object_at(loc2)
        self.assertEqual(obj1, None)

    def testGetObjectAtNone2(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.remove_object("tree", loc1)

        obj1 = state.get_object_at(loc1)
        self.assertEqual(obj1, None)

    def testGetObjectAtNone3(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.remove_object("tree", loc1)
        state.place_object("chest", properties={"loc": loc1})

        obj1 = state.get_object_at(loc1)
        self.assertEqual(obj1.type, "chest")

    def testUpdateObjectLoc(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.update_object_loc(loc1, loc2)
        obj_type_id = state.item_encoder.get_id("tree")

        self.assertEqual(state._map[loc2], obj_type_id)
        self.assertEqual(state._map[loc1], 0)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testUpdateObjectLoc2(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (4, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.update_object_loc(loc1, loc2)
        obj_type_id = state.item_encoder.get_id("tree")

        self.assertEqual(state._map[loc2], obj_type_id)
        self.assertEqual(state._map[loc1], 0)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

        state.place_object("tree", properties={"loc": loc1})
        self.assertEqual(state._map[loc1], 1)
        self.assertEqual(len(state._objects[obj_type_id]), 2)
    
    def testUpdateObjectLocCollision(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (3, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc2})
        res = state.update_object_loc(loc1, loc2)
        self.assertEqual(res, False)
        obj_type_id = state.item_encoder.get_id("tree")

        self.assertEqual(state._map[loc2], obj_type_id)
        self.assertEqual(state._map[loc1], obj_type_id)
        self.assertEqual(len(state._objects[obj_type_id]), 2)

    def testPlaceObjectCollision(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.place_object("tree", properties={"loc": loc1})
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc1], 1)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testGetObjectState(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})
        res = state.get_object_state(loc1)
        self.assertEqual(res, "block")

    def testUpdateObjectState(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        state.place_object("tree", properties={"loc": loc1})
        state.update_object_state(loc1)
        obj = state.get_object_at(loc1)
        self.assertEqual(obj.state, "floating")
        state.update_object_state(loc1)
        obj = state.get_object_at(loc1)
        self.assertEqual(obj.state, "block")

    def testReset(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        self.assertEqual((state._map == 1).sum(), 3)
        self.assertEqual(len(state._objects[1]), 3)

        state.random_place(object_str="chest", count=1)
        self.assertEqual((state._map == 2).sum(), 1)
        self.assertEqual(len(state._objects[2]), 1)
        state.reset()
        self.assertEqual(len(state._objects[1]), 0)
        self.assertEqual(len(state._objects[2]), 0)
        # self.assertEqual(True, False)


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

