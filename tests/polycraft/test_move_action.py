import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject

class MoveTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state)
        }
    
    def testMove(self):
        """
        Tests moving in four directions
        """
        obj: Entity = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        self.actions["up"].do_action(obj)
        self.assertEqual(obj.loc, (0, 2))
        self.assertEqual(obj.facing, "NORTH")

        self.actions["left"].do_action(obj)
        self.assertEqual(obj.loc, (0, 1))
        self.assertEqual(obj.facing, "WEST")

        self.actions["down"].do_action(obj)
        self.assertEqual(obj.loc, (1, 1))
        self.assertEqual(obj.facing, "SOUTH")

        self.actions["right"].do_action(obj)
        self.assertEqual(obj.loc, (1, 2))
        self.assertEqual(obj.facing, "EAST")

        self.state.clear()


    def testMoveHitEdge(self):
        """
        Tests out of bound
        """
        # top
        obj_topedge = self.state.place_object("agent", Entity, properties={"loc": (0, 2)})
        self.assertFalse(self.actions["up"].check_precondition(obj_topedge))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["up"].do_action(obj_topedge))
        self.assertEqual(obj_topedge.loc, (0, 2))

        # bottom
        obj_bottomedge = self.state.place_object("agent", Entity, properties={"loc": (4, 2)})
        self.assertFalse(self.actions["down"].check_precondition(obj_bottomedge))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["down"].do_action(obj_bottomedge))
        self.assertEqual(obj_bottomedge.loc, (4, 2))

        # left
        obj_leftedge = self.state.place_object("agent", Entity, properties={"loc": (2, 0)})
        self.assertFalse(self.actions["left"].check_precondition(obj_leftedge))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["left"].do_action(obj_leftedge))
        self.assertEqual(obj_leftedge.loc, (2, 0))

        # right
        obj_rightedge = self.state.place_object("agent", Entity, properties={"loc": (2, 7)})
        self.assertFalse(self.actions["right"].check_precondition(obj_rightedge))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["right"].do_action(obj_rightedge))
        self.assertEqual(obj_rightedge.loc, (2, 7))

        # clear everything
        self.state.clear()

    def testMoveCollide(self):
        """
        Create obstacle around the agent except for the down direction.
        Should work when going down and should raise exceptions otherwise.
        """
        pogoist1 = self.state.place_object("pogoist1", Entity, properties={"loc": (2, 1)})
        pogoist2 = self.state.place_object("pogoist2", Entity, properties={"loc": (2, 3)})
        tree1 = self.state.place_object("tree", properties={"loc": (1, 2)})
        agent = self.state.place_object("pogoist2", Entity, properties={"loc": (2, 2)})

        self.assertFalse(self.actions["right"].check_precondition(agent))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["right"].do_action(agent))
        self.assertEqual(agent.loc, (2, 2))

        self.assertFalse(self.actions["left"].check_precondition(agent))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["right"].do_action(agent))
        self.assertEqual(agent.loc, (2, 2))

        self.assertFalse(self.actions["up"].check_precondition(agent))
        # self.assertRaises(PreconditionNotMetError, 
        #     lambda: self.actions["right"].do_action(agent))
        self.assertEqual(agent.loc, (2, 2))

        self.assertTrue(self.actions["down"].check_precondition(agent))
        self.actions["down"].do_action(agent)
        self.assertEqual(agent.loc, (3, 2))
        
    def testPickupMove(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {}
        obj = self.state.place_object("tree", PolycraftObject, properties={"loc": (0, 2)})
        self.actions["up"].do_action(agent, obj)
        self.actions["break"].do_action(agent, obj)
        hbn = self.state.get_object_at((0,2))
        self.assertEqual(hbn.state, "floating")
        self.actions["up"].do_action(agent, obj)
        self.assertEqual(agent.inventory["tree"], 1)
        self.actions["down"].do_action(agent, obj)

        