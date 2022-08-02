import unittest
import numpy as np
import json
from gym_novel_gridworlds2.contrib.polycraft.states.polycraft_state import (
    PolycraftState,
)
from gym_novel_gridworlds2.object.entity import Entity

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.state.state import LocationOccupied


class StateTestPlacement(unittest.TestCase):
    def testPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        obj_type_id = state.item_encoder.get_id("tree")
        print(state._map[loc].get_obj_entities())
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testPlaceItemOverItem(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        self.assertRaises(
            LocationOccupied,
            lambda: state.place_object("tree", properties={"loc": loc}),
        )
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testPlaceItemOverItem2(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        self.assertRaises(
            LocationOccupied,
            lambda: state.place_object("chest", properties={"loc": loc}),
        )
        obj_type_id_1 = state.item_encoder.get_id("tree")
        obj_type_id_2 = state.item_encoder.get_id("chest")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id_1]), 1)
        self.assertTrue(obj_type_id_2 not in state._objects)

    def testPlaceEntityOverItem(self):
        """
        Should now throw an error
        TODO
        """
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc, "state": "floating"})
        state.place_object("trader", Entity, properties={"loc": loc})
        obj_entities = state._map[loc].get_obj_entities()
        obj_type_id_1 = state.item_encoder.get_id("tree")
        obj_type_id_2 = state.item_encoder.get_id("trader")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        print(state._map[loc].get_obj_entities()[1][0])
        self.assertEqual(state._map[loc].get_obj_entities()[1][0].type, "trader")
        self.assertEqual(state._map[loc].get_obj_entities()[1][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id_1]), 1)
        self.assertEqual(len(state._objects[obj_type_id_2]), 1)

    def testPlaceEntityOverBlockItem(self):
        """
        Should now throw an error
        TODO
        """
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        self.assertRaises(
            LocationOccupied,
            lambda: state.place_object("tree", Entity, properties={"loc": loc}),
        )
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testPlaceTwoItems(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        loc2 = (3, 4)
        state.place_object("tree", properties={"loc": loc})
        state.place_object("chest", properties={"loc": loc2})

        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(state._map[loc2].get_obj_entities()[0][0].type, "chest")
        self.assertEqual(state._map[loc2].get_obj_entities()[0][0].loc, loc2)
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

    def testrandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=2)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 2)

    def testrandomPlaceItemFull(self):
        state = State(map_size=(2, 2), objects=[])
        state.random_place(object_str="tree", count=5)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 4)

    def testDoubleRandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=2)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 2)

        state.random_place(object_str="chest", count=1)
        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

    def testMultipleRandomPlaceItem(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 3)

        state.random_place(object_str="chest", count=1)
        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

        state.random_place(object_str="crafting_table", count=1)
        obj_type_id3 = state.item_encoder.get_id("crafting_table")
        self.assertEqual(len(state._objects[obj_type_id3]), 1)

        state.random_place(object_str="iron", count=2)
        obj_type_id4 = state.item_encoder.get_id("iron")
        self.assertEqual(len(state._objects[obj_type_id4]), 2)

    def testMultipleRandomPlaceItemFull(self):
        state = State(map_size=(2, 2), objects=[])
        state.random_place(object_str="tree", count=3)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 3)

        state.random_place(object_str="chest", count=1)
        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

        state.random_place(object_str="crafting_table", count=1)
        self.assertEqual(len(state._objects[obj_type_id1]), 3)
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

        state.random_place(object_str="iron", count=2)
        self.assertEqual(len(state._objects[obj_type_id1]), 3)
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

    def testRemoveObject(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

        state.remove_object("tree", loc)
        self.assertEqual(len(state._map[loc].get_obj_entities()[0]), 0)
        self.assertEqual(len(state._objects[obj_type_id]), 0)

    def testRemoveIllegalObject(self):
        state = State(map_size=(5, 5), objects=[])
        loc = (2, 3)
        state.place_object("tree", properties={"loc": loc})
        obj_type_id = state.item_encoder.get_id("tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

        state.remove_object("car", loc)
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc].get_obj_entities()[0][0].loc, loc)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    # should fail:
    # def testRemoveWrongObject(self):
    #     state = State(map_size=(5, 5), objects=[])
    #     loc1 = (2, 3)
    #     loc2 = (3, 3)
    #     state.place_object("tree", properties={"loc": loc1})

    #     obj_type_id1 = state.item_encoder.get_id("tree")
    #     self.assertEqual(state._map[loc1].get_obj_entities()[0][0], obj_type_id1)
    #     self.assertEqual(len(state._objects[obj_type_id1]), 1)

    #     state.remove_object("tree", loc2)
    #     self.assertEqual(state._map[loc1].get_obj_entities()[0][0], 1)
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
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].loc, loc1)
        self.assertEqual(len(state._map[loc2].get_obj_entities()[0]), 0)
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
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].loc, loc1)
        self.assertEqual(len(state._map[loc2].get_obj_entities()[0]), 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 1)

        state.remove_object("tree", loc1)
        self.assertEqual(len(state._map[loc1].get_obj_entities()[0]), 0)
        self.assertEqual(len(state._objects[obj_type_id1]), 0)

    def testGetObjectsRandom(self):
        state = State(map_size=(5, 5), objects=[])
        state.random_place(object_str="tree", count=3)
        obj_type_id1 = state.item_encoder.get_id("tree")
        self.assertEqual(len(state._objects[obj_type_id1]), 3)

        state.random_place(object_str="chest", count=1)
        obj_type_id2 = state.item_encoder.get_id("chest")
        self.assertEqual(len(state._objects[obj_type_id2]), 1)

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

        self.assertEqual(state._map[loc2].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(len(state._map[loc1].get_obj_entities()[0]), 0)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

    def testUpdateObjectLoc2(self):
        state = State(map_size=(5, 5), objects=[])
        loc1 = (2, 3)
        loc2 = (4, 4)
        state.place_object("tree", properties={"loc": loc1})
        state.update_object_loc(loc1, loc2)
        obj_type_id = state.item_encoder.get_id("tree")

        self.assertEqual(state._map[loc2].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(len(state._map[loc1].get_obj_entities()[0]), 0)
        self.assertEqual(len(state._objects[obj_type_id]), 1)

        state.place_object("tree", properties={"loc": loc1})
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].type, "tree")
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

        self.assertEqual(state._map[loc2].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(state._map[loc1].get_obj_entities()[0][0].type, "tree")
        self.assertEqual(len(state._objects[obj_type_id]), 2)

    def testInitBorderMulti(self):
        state = PolycraftState(map_size=(5, 5), objects=[])
        state.init_border([0, 0], [4, 4])

        self.assertEqual(state._map[(0, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(0, 1)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(0, 2)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(0, 3)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(0, 4)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(0, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(1, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(2, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(3, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 0)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(4, 1)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 2)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 3)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 4)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(1, 4)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(2, 4)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(3, 4)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 4)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(1, 3)], None)
        self.assertEqual(state._map[(2, 3)], None)
        self.assertEqual(state._map[(3, 3)], None)
        self.assertEqual(state._map[(1, 2)], None)
        self.assertEqual(state._map[(2, 2)], None)
        self.assertEqual(state._map[(3, 2)], None)
        self.assertEqual(state._map[(1, 1)], None)
        self.assertEqual(state._map[(2, 1)], None)
        self.assertEqual(state._map[(3, 1)], None)

    def testInitBorderMulti2(self):
        state = PolycraftState(map_size=(10, 10), objects=[])
        state.init_border([4, 0], [9, 9])

        self.assertEqual(state._map[(4, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 1)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 2)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 3)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 4)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 5)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 6)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 7)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 8)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(4, 9)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(5, 9)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(6, 9)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(7, 9)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(8, 9)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 9)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(9, 8)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 7)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 6)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 5)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 4)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 3)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 2)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 1)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(9, 0)].get_obj_entities()[0][0].type, "bedrock")

        self.assertEqual(state._map[(8, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(7, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(6, 0)].get_obj_entities()[0][0].type, "bedrock")
        self.assertEqual(state._map[(5, 0)].get_obj_entities()[0][0].type, "bedrock")

    # def testGetObjectState(self):
    #     state = State(map_size=(5, 5), objects=[])
    #     loc1 = (2, 3)
    #     state.place_object("tree", properties={"loc": loc1})
    #     res = state.get_object_state(loc1)
    #     self.assertEqual(res, "block")

    # def testUpdateObjectState(self):
    #     state = State(map_size=(5, 5), objects=[])
    #     loc1 = (2, 3)
    #     state.place_object("tree", properties={"loc": loc1})
    #     state.update_object_state(loc1)
    #     obj = state.get_object_at(loc1)
    #     self.assertEqual(obj.state, "floating")
    #     state.update_object_state(loc1)
    #     obj = state.get_object_at(loc1)
    #     self.assertEqual(obj.state, "block")

    # def testReset(self):
    #     state = State(map_size=(5, 5), objects=[])
    #     state.random_place(object_str="tree", count=3)
    #     self.assertEqual((state._map == 1).sum(), 3)
    #     self.assertEqual(len(state._objects[1]), 3)

    #     state.random_place(object_str="chest", count=1)
    #     self.assertEqual((state._map == 2).sum(), 1)
    #     self.assertEqual(len(state._objects[2]), 1)
    #     state.reset()
    #     self.assertEqual(len(state._objects[1]), 0)
    #     self.assertEqual(len(state._objects[2]), 0)


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
