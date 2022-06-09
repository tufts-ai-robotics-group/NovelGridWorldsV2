import unittest
import numpy as np 
import json

from gym_novel_gridworlds2.state import State

class StateTestLoadJSON(unittest.TestCase):
    def setUp(self):
        with open("sample_state.json") as f:
            data = json.load(f)
            self.state = State(map_json=data)

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

