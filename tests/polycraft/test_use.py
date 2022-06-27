import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.use import Use
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.contrib.polycraft.objects.chest import Chest


class UseTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state),
            "use": Use(state=self.state),
        }

    def testUseDoor(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object("door", Door, properties={"loc": (0, 2)})

        self.actions["use"].do_action(agent, obj)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.canWalkOver, True)

        self.state.clear()

    def testUseChest(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object("chest", Chest, properties={"loc": (0, 2)})

        self.actions["use"].do_action(agent, obj)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.inventory, {})

        self.state.clear()

    def testUseDoorThenMove(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object("door", Door, properties={"loc": (0, 2)})

        self.actions["use"].do_action(agent, obj)

        self.actions["up"].do_action(agent, obj)

        hbn = self.state.get_objects_at((0, 2))
        self.assertEqual(hbn[0][0].type, "door")
        self.assertEqual(hbn[1][0].type, "agent")
        print(hbn)

        self.actions["down"].do_action(agent, obj)
        hbn1 = self.state.get_objects_at((1, 2))
        hbn2 = self.state.get_objects_at((0, 2))
        self.assertEqual(hbn1[0][0].type, "door")
        self.assertEqual(hbn2[1][0].type, "agent")

        self.actions["down"].do_action(agent, obj)
        hbn1 = self.state.get_objects_at((2, 2))
        hbn2 = self.state.get_objects_at((1, 2))
        print(hbn1)
        print(hbn2)
        self.assertEqual(hbn2[0][0].type, "door")
        self.assertEqual(hbn2[1][0].type, "agent")

        self.state.clear()
