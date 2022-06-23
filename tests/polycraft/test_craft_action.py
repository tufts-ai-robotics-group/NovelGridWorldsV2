import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject


class CraftTests(unittest.TestCase):
    def setUp(self):
        self.state = State(map_size=(5, 8), objects=[])
        recipe_dict = {
        "recipes": {
            "stick": {
              "input": [
                {"plank": 2}
              ],
              "output": [
                {"stick": 4}
              ]
            },
            "plank": {
              "input": [
                {"tree": 1}
              ],
              "output": [
                {"plank": 4}
              ]
            },
            "pogo_stick": {
              "input": [
                {"stick": 4},
                {"plank": 2},
                {"rubber": 1}
              ],
              "output": [
                {"pogo_stick": 1}
              ]
            }
        }}
        """How to parse the recipe dict and convert it to actions"""
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state)
        }
        items = list(recipe_dict["recipes"].keys())
        for i in range(len(items)):
            craftStr = "craft_" + items[i]
            self.actions[craftStr] = Craft(state=self.state, recipe=recipe_dict["recipes"][items[i]])
        """End section"""
    
    def testCraftStick(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"plank" : 2}
        self.actions["craft_stick"].do_action(agent)

        self.assertEqual(agent.inventory["stick"], 4)
        self.assertEqual(agent.inventory["plank"], 0)

        self.state.clear()

    def testCraftStickExits(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"plank" : 2, "stick": 4, "rubber": 1}
        self.actions["craft_stick"].do_action(agent)

        self.assertEqual(agent.inventory["stick"], 8)
        self.assertEqual(agent.inventory["plank"], 0)
        self.assertEqual(agent.inventory["rubber"], 1)

        self.state.clear()

    def testCraftPogoStick(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"plank" : 2, "stick": 4, "rubber": 1}
        self.actions["craft_pogo_stick"].do_action(agent)

        self.assertEqual(agent.inventory["pogo_stick"], 1)
        self.assertEqual(agent.inventory["stick"], 0)
        self.assertEqual(agent.inventory["plank"], 0)
        self.assertEqual(agent.inventory["rubber"], 0)

        self.state.clear()

    def testCraftBoth(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"plank" : 4, "rubber": 1}
        self.actions["craft_stick"].do_action(agent)
        self.actions["craft_pogo_stick"].do_action(agent)

        self.assertEqual(agent.inventory["pogo_stick"], 1)
        self.assertEqual(agent.inventory["stick"], 0)
        self.assertEqual(agent.inventory["plank"], 0)
        self.assertEqual(agent.inventory["rubber"], 0)

        self.state.clear()

    def testBreakAndCraft(self):
        agent = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})
        agent.inventory = {"rubber": 1}
        obj = self.state.place_object("tree", PolycraftObject, properties={"loc": (0, 2)})
        self.actions["break"].do_action(agent, obj)
        hbn = self.state.get_object_at((0,2))
        self.assertEqual(hbn.state, "floating")
        self.actions["up"].do_action(agent, obj)

        self.actions["craft_plank"].do_action(agent)
        self.assertEqual(agent.inventory["plank"], 4)

        self.actions["craft_stick"].do_action(agent)
        self.assertEqual(agent.inventory["stick"], 4)
        self.assertEqual(agent.inventory["plank"], 2)

        self.actions["craft_pogo_stick"].do_action(agent)
        self.assertEqual(agent.inventory["pogo_stick"], 1)
        self.assertEqual(agent.inventory["stick"], 0)
        self.assertEqual(agent.inventory["plank"], 0)
        self.assertEqual(agent.inventory["rubber"], 0)

    
        

        