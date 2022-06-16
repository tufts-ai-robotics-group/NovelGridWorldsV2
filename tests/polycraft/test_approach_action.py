import unittest

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions import Move, Break, Approach
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.object.entity import Entity

import numpy as np


class ApproachTestSimple(unittest.TestCase):
    """
        Test map No.1: simple approach
        The map 
        +---+---+---+---+---+---+---+
        |   | 0 | 1 | 2 | 3 | 4 | 5 |
        +---+---+---+---+---+---+---+
        | 0 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 1 |   |   |   |   | o |   |
        +---+---+---+---+---+---+---+
        | 2 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 3 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 4 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 5 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 6 |   |   |   |   |   |   |
        +---+---+---+---+---+---+---+
        | 7 |   |   |   | a |   |   |
        +---+---+---+---+---+---+---+
        a = agent, o = obj
    """

    def setUp(self):
        self.state = State(map_size=(8, 6), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "approach": Approach(state=self.state)
        }
        self.agent: Entity = self.state.place_object("agent", Entity, properties={"loc": (7, 3)})
        self.obj = self.state.place_object("tree", PolycraftObject, properties={"loc": (1, 4)})
    

    def testSimpleApproachDistance1(self):
        """
        tests simple approch. no obstructions in the map.
        """

        approach: Approach = self.actions['approach']
        approach.do_action(self.agent, "tree", distance=1)

        self.assertIn((self.agent.facing, self.agent.loc), [
            ("NORTH", (2, 4)),
            ("WEST", (1, 5)),
            ("SOUTH", (0, 4)),
            ("EAST", (1, 3))
        ])
    

    def testSimpleApproachDistance2(self):
        """
        tests simple approch. no obstructions in the map.
        """
        approach: Approach = self.actions['approach']
        approach.do_action(self.agent, "tree", distance=2)

        self.assertIn((self.agent.facing, self.agent.loc), [
            ("NORTH", (3, 4)),
            ("EAST", (1, 2))
        ])


        
class ApproachTestSomeObstacles(unittest.TestCase):
    """
        Test map No.1: simple approach
        The map 
        +---+---+---+---+---+---+---+
        |   | 0 | 1 | 2 | 3 | 4 | 5 |
        +---+---+---+---+---+---+---+
        | 0 |   |   | B |   |   |   |
        +---+---+---+---+---+---+---+
        | 1 | > | > | v | B | o | < |
        +---+---+---+---+---+---+---+
        | 2 | ^ | B | > | v | B | ^ |
        +---+---+---+---+---+---+---+
        | 3 | ^ | B | B | v | B | ^ |
        +---+---+---+---+---+---+---+
        | 4 | ^ | B | B | v | B | ^ |
        +---+---+---+---+---+---+---+
        | 5 | ^ | B | B | > | > | ^ |
        +---+---+---+---+---+---+---+
        | 6 | ^ | B |   |   | B | B |
        +---+---+---+---+---+---+---+
        | 7 | a | B |   |   | B | p |
        +---+---+---+---+---+---+---+
        a = agent, o = obj
        B = barrier
        ^><v = path
        p = unreachable object
    """

    def setUp(self):
        self.state = State(map_size=(8, 6), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "approach": Approach(state=self.state)
        }
        barrier_locs = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
            (0, 2), (3, 2), (4, 2), (5, 2), (2, 4), (3, 4), (4, 4), (6, 4),
            (7, 4), (6, 5), (1, 3)
        ]
        for loc in barrier_locs:
            self.state.place_object("barrier", PolycraftObject, properties={"loc": loc})
        # reachable tree
        self.state.place_object("tree", PolycraftObject, properties={"loc": (1, 4)})
        # unreachable tree
        self.state.place_object("tree2", PolycraftObject, properties={"loc": (7, 5)})
        self.agent: Entity = self.state.place_object("agent", Entity, properties={"loc": (7, 3)})
    

    def testSimpleApproachComplicatedPath(self):
        approach: Approach = self.actions['approach']
        approach.do_action(self.agent, "tree", distance=1)

        self.assertIn((self.agent.facing, self.agent.loc), [
            ("WEST", (1, 5)),
            ("SOUTH", (0, 4)),
        ])
    

    def testSimpleApproachUnreachable(self):
        approach: Approach = self.actions['approach']
        approach.do_action(self.agent, "tree2", distance=2)

        # shouldn't move
        self.assertEqual((self.agent.facing, self.agent.loc), ('EAST', (7, 3)))


