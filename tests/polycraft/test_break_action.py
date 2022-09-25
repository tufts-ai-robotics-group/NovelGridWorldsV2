import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.smoothmove import SmoothMove as Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door


class BreakTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state),
        }

    def testBreak(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (0, 2)}
        )
        self.actions["break"].do_action(agent)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.state, "floating")

        self.state.clear()

    def testBreakFloating(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (0, 2)}
        )
        self.actions["break"].do_action(agent, obj)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.state, "floating")

        self.assertRaises(
            PreconditionNotMetError, lambda: self.actions["break"].do_action(agent, obj)
        )

        self.state.clear()

    def testBreakWrongWays(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (2, 2)}
        )
        obj2 = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (1, 3)}
        )
        obj3 = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (1, 1)}
        )

        self.assertRaises(
            PreconditionNotMetError, lambda: self.actions["break"].do_action(agent, obj)
        )
        self.assertRaises(
            PreconditionNotMetError,
            lambda: self.actions["break"].do_action(agent, obj2),
        )
        self.assertRaises(
            PreconditionNotMetError,
            lambda: self.actions["break"].do_action(agent, obj3),
        )

        self.state.clear()

    def testBreakTooFar(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (2, 2)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (0, 2)}
        )

        self.assertRaises(
            PreconditionNotMetError, lambda: self.actions["break"].do_action(agent, obj)
        )

        self.state.clear()

    def testMoveAndBreak(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (2, 2)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (0, 2)}
        )
        self.actions["up"].do_action(agent)
        self.actions["break"].do_action(agent)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.state, "floating")

        self.state.clear()

    def testMoveAndBreak2(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (2, 1)})
        obj = self.state.place_object(
            "tree", PolycraftObject, properties={"loc": (0, 2)}
        )
        self.actions["up"].do_action(agent)
        self.actions["right"].do_action(agent)
        self.actions["up"].do_action(agent)
        self.actions["break"].do_action(agent)

        hbn = self.state.get_object_at((0, 2))
        self.assertEqual(hbn.state, "floating")

        self.state.clear()

    def testBreakBedrock(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object(
            "bedrock", PolycraftObject, properties={"loc": (0, 2)}
        )

        self.assertRaises(
            PreconditionNotMetError, lambda: self.actions["break"].do_action(agent, obj)
        )

        self.state.clear()

    def testBreakDoor(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object(
            "door", PolycraftObject, properties={"loc": (0, 2)}
        )
        hbn = self.state.get_object_at((0, 2))
        print(hbn)

        self.actions["break"].do_action(agent)

        hbn = self.state.get_object_at((0, 2))
        print(hbn)

        # self.assertEqual(True, False)

        self.state.clear()
