import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.smoothmove import SmoothMove as Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.select_item import SelectItem
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door


class SelectItemTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state),
            "select_item": SelectItem(state=self.state),
        }

    def testSelect1(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"tree": 1}
        self.actions["select_item"].do_action(agent, "tree")

        self.assertEqual(agent.selectedItem, "tree")

        self.state.clear()

    def testSelectInvalid(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"door": 1}

        self.assertRaises(
            PreconditionNotMetError,
            lambda: self.actions["select_item"].do_action(agent, "tree"),
        )

        self.assertEqual(agent.selectedItem, None)

        self.state.clear()
