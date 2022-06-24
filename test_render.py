from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

import numpy as np

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.utils.json_parser import ConfigParser

class TestRender():
    def setUp(self):
        self.state = State(map_size=(8, 8), objects=[])
        self.state.init_border()
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
        # parser = ConfigParser()
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state),
            "craft_stick": Craft(state=self.state, recipe=recipe_dict["recipes"]["stick"]),
            "craft_plank": Craft(state=self.state, recipe=recipe_dict["recipes"]["plank"]),
            "craft_pogo_stick": Craft(state=self.state, recipe=recipe_dict["recipes"]["pogo_stick"])
        }
        # self.actions.update(parser.parse_recipe(self.state, recipe_dict["recipes"]))
        pogoist: Entity = self.state.place_object("agent", Entity, properties={"loc": (2, 2)})
        pogoist.inventory = {"tree": 1, "rubber": 1}
        self.state.random_place("tree", 3, PolycraftObject)
        self.state.random_place("rubber", 1, PolycraftObject)

    def getSymbol(self, obj, state):
        if obj == "tree":
            if state == "block":
                return 'T'
            else:
                return 't'
        elif obj == "air":
            return ' '
        elif obj == "bedrock":
            return 'X'
        elif obj == "rubber":
            if state == "block":
                return 'R'
            else:
                return 'r'
        elif obj == "agent":
            return 'A'
        else:
            return ' '

    def mapRepresentation(self):
        res: np.ndarray = np.empty(self.state.initial_info["map_size"], dtype="object")
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                obj = self.state.get_objects_at((i,j))
                if len(obj[0]) != 0:
                    res[i][j] = self.getSymbol(obj[0][0].type, obj[0][0].state)
                elif len(obj[1]) != 0:
                    res[i][j] = self.getSymbol(obj[1][0].type, obj[1][0].state)
                else:
                    res[i][j] = ' '
        print(res)

    def mainLoop(self):
        won = False
        while not won:
            agent = self.state.get_objects_of_type("agent")[0]
            if "pogo_stick" in agent.inventory:
                won = True
                print("You won!")
            else:
                self.mapRepresentation()
                print("")
                print("Agent's Inventory:")
                print(agent.inventory)
                print("")
                print("Actions: up, down, left, right, break, craft_stick, craft_plank, craft_pogo_stick")
                choice = input("Select an action: ")
                if choice == "up":
                    self.actions["up"].do_action(agent)
                elif choice == "down":
                    self.actions["down"].do_action(agent)
                elif choice == "left":
                    self.actions["left"].do_action(agent)
                elif choice == "right":
                    self.actions["right"].do_action(agent)
                elif choice == "break":
                    self.actions["break"].do_action(agent)
                elif choice == "craft_stick":
                    self.actions["craft_stick"].do_action(agent)
                elif choice == "craft_plank":
                    self.actions["craft_plank"].do_action(agent)
                elif choice == "craft_pogo_stick":
                    self.actions["craft_pogo_stick"].do_action(agent)

def main():
    test = TestRender()
    test.setUp()
    test.mainLoop()

if __name__ == '__main__':
    main()