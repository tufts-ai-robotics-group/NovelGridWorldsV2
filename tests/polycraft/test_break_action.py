import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break import Break
from gym_novel_gridworlds2.object.entity import Entity

class BreakTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state)
        }
    
    def testBreak(self):
        """
        Tests moving in four directions
        """
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        obj = self.state.place_object("tree", properties={"loc": (0, 2)})
        self.actions["break"].do_action(agent, obj)

        self.state.clear()


    
        

        