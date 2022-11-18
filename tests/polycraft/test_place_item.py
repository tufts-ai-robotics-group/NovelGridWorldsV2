import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.smoothmove import (
    SmoothMove as Move,
)
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.use import Use
from gym_novel_gridworlds2.contrib.polycraft.actions.select_item import SelectItem
from gym_novel_gridworlds2.contrib.polycraft.actions.place_item import PlaceItem
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects import Chest, Door, TreeTap
from gym_novel_gridworlds2.state.dynamic import Dynamic


class PlaceItemTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(10, 10), objects=[])
        self.obj_types = {
            "chest": {"module": Chest, "params": {}},
            "crafting_table": {"module": PolycraftObject, "params": {}},
            "door": {"module": Door, "params": {}},
            "default": {"module": PolycraftObject, "params": {}},
            "tree_tap": {"module": TreeTap, "params": {}},
        }

        self.dynamics = Dynamic(None, None, None, self.obj_types, None)

        self.actions = {
            "up": Move(direction="W", state=self.state),
            "down": Move(direction="X", state=self.state),
            "left": Move(direction="A", state=self.state),
            "right": Move(direction="D", state=self.state),
            "break": Break(state=self.state),
            "use": Use(state=self.state),
            "select_item": SelectItem(state=self.state),
            "place_item": PlaceItem(state=self.state, dynamics=self.dynamics),
        }

    def testPlace1(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"tree": 1}
        self.actions["select_item"].do_action(agent, "tree")

        self.assertEqual(agent.selectedItem, "tree")

        self.actions["place_item"].do_action(agent, "tree")

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.type, "tree")

        self.assertEqual(agent.inventory[agent.selectedItem], 0)

        self.state.clear()

    def testPlace2(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"tree": 2}
        self.actions["select_item"].do_action(agent, "tree")

        self.assertEqual(agent.selectedItem, "tree")

        self.actions["place_item"].do_action(agent, "tree")

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.type, "tree")

        self.assertEqual(agent.inventory[agent.selectedItem], 1)

        self.actions["right"].do_action(agent)

        self.actions["place_item"].do_action(agent, "tree")

        hbn = self.state.get_object_at((0, 3))
        self.assertEqual(hbn.type, "tree")

        self.assertEqual(agent.inventory[agent.selectedItem], 0)

        self.state.clear()

    def testPlaceOver(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"tree": 2}
        self.actions["select_item"].do_action(agent, "tree")

        self.assertEqual(agent.selectedItem, "tree")

        self.actions["place_item"].do_action(agent, "tree")

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.type, "tree")

        self.assertEqual(agent.inventory[agent.selectedItem], 1)

        self.assertRaises(
            PreconditionNotMetError,
            lambda: self.actions["place_item"].do_action(agent),
        )

        self.assertEqual(agent.inventory[agent.selectedItem], 1)

        self.state.clear()

    def testPlaceTreeTap(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"oak_log": 2, "tree_tap": 1}

        # try to place tree tap without tree
        self.actions["select_item"].do_action(agent, "tree_tap")
        self.assertEqual(agent.selectedItem, "tree_tap")
        self.assertRaises(
            PreconditionNotMetError,
            lambda: self.actions["place_item"].do_action(agent, "tree_tap"),
        )
        self.assertEqual(agent.inventory["tree_tap"], 1)

        # place tree
        self.actions["select_item"].do_action(agent, "oak_log")
        self.assertEqual(agent.selectedItem, "oak_log")
        self.actions["place_item"].do_action(agent, "oak_log")
        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.type, "oak_log")
        self.assertEqual(agent.inventory[agent.selectedItem], 1)

        # go right and place a treetap next to the tree
        self.actions["right"].do_action(agent)
        self.actions["place_item"].do_action(agent, "tree_tap")

        hbn = self.state.get_object_at((0, 3))
        self.assertEqual(hbn.type, "tree_tap")
        self.assertEqual(agent.inventory["tree_tap"], 0)

    def testPlaceDoor(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"door": 1}
        self.actions["select_item"].do_action(agent, "door")

        self.assertEqual(agent.selectedItem, "door")

        self.actions["place_item"].do_action(agent, "door")

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.type, "door")
        self.assertEqual(hbn.canWalkOver, False)

        self.actions["use"].do_action(agent)

        self.actions["up"].do_action(agent)

        self.assertEqual(agent.inventory[agent.selectedItem], 0)

        self.state.clear()

    def testPlaceCraftingTable(self):
        ctable = self.state.place_object(
            "crafting_table", PolycraftObject, properties={"loc": (0, 2)}
        )
        agent = self.state.place_object(
            "agent", Entity, properties={"loc": (ctable.loc[0] + 1, ctable.loc[1])},
        )

        print("AGENT: ", agent.loc)

        hbn = self.state.get_object_at(ctable.loc)
        self.assertEqual(hbn.type, "crafting_table")

        self.actions["break"].do_action(agent, hbn)
        self.actions["up"].do_action(agent)

        ctable2 = self.state.get_objects_of_type("crafting_table")
        self.assertEqual(ctable2, [])

        print("LOC1: ", ctable.loc)

        print("AGENT: ", agent.loc)
        print(agent.inventory)

        self.actions["select_item"].do_action(agent, "crafting_table")

        self.actions["down"].do_action(agent)
        self.actions["down"].do_action(agent)
        self.actions["down"].do_action(agent)
        self.actions["up"].do_action(agent)

        self.assertEqual(agent.selectedItem, "crafting_table")

        print("AGENT: ", agent.loc)

        self.actions["place_item"].do_action(agent, "crafting_table")

        new_ctable = self.state.get_objects_of_type("crafting_table")
        self.assertNotEqual(new_ctable, [])

        print(agent.inventory)

        print("LOC2: ", ctable.loc)

        hbn = self.state.get_object_at(ctable.loc)
        self.assertEqual(hbn, None)

        self.state.clear()

    def testPlaceCraftingTableUsingParser(self):
        self.state.random_place_in_room(
            "crafting_table", 1, [0, 0], [5, 8], PolycraftObject, properties=dict()
        )
        ctable = self.state.get_objects_of_type("crafting_table")[0]
        print("LOC1: ", ctable.loc)

        agent = self.state.place_object(
            "agent", Entity, properties={"loc": (ctable.loc[0] + 1, ctable.loc[1])},
        )

        print("AGENT: ", agent.loc)

        hbn = self.state.get_object_at(ctable.loc)
        self.assertEqual(hbn.type, "crafting_table")

        self.actions["break"].do_action(agent, hbn)

        self.actions["up"].do_action(agent)

        ctable2 = self.state.get_objects_of_type("crafting_table")
        self.assertEqual(ctable2, [])

        print("LOC2: ", ctable.loc)

        print("AGENT: ", agent.loc)
        print(agent.inventory)

        self.actions["select_item"].do_action(agent, "crafting_table")

        self.actions["down"].do_action(agent)
        self.actions["down"].do_action(agent)
        self.actions["down"].do_action(agent)
        self.actions["up"].do_action(agent)

        self.assertEqual(agent.selectedItem, "crafting_table")

        print("AGENT: ", agent.loc)

        self.actions["place_item"].do_action(agent, "crafting_table")

        new_ctable = self.state.get_objects_of_type("crafting_table")
        self.assertNotEqual(new_ctable, [])

        print(agent.inventory)

        print("LOC3: ", ctable.loc)

        hbn = self.state.get_object_at(ctable.loc)
        self.assertEqual(hbn, None)

        self.state.clear()

        # raise Exception("")

