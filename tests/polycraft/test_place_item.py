import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.use import Use
from gym_novel_gridworlds2.contrib.polycraft.actions.select_item import SelectItem
from gym_novel_gridworlds2.contrib.polycraft.actions.place_item import PlaceItem
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects import Chest, Door
from gym_novel_gridworlds2.state.dynamic import Dynamic


class PlaceItemTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.obj_types = {
            "chest": {"module": Chest, "params": {}},
            "door": {"module": Door, "params": {}},
            "default": {"module": PolycraftObject, "params": {}},
        }

        self.dynamics = Dynamic(None, None, None, self.obj_types)

        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
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

        hbn = self.state.get_object_at((1, 4))
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

    def testPlaceProperties(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"tree": 1}
        self.actions["select_item"].do_action(agent, "tree")

        self.assertEqual(agent.selectedItem, "tree")

        self.actions["place_item"].do_action(agent, "tree")

        self.actions["break"].do_action(agent)

        self.actions["up"].do_action(agent)

        self.assertEqual(agent.inventory[agent.selectedItem], 1)

        self.state.clear()

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
