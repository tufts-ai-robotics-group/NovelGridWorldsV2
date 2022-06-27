from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

import numpy as np
import time

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.contrib.polycraft.actions.use import Use
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.contrib.polycraft.objects.chest import Chest

class TestRender():
    def setUp(self):

        """
        #EASY
        self.state = State(map_size=(8, 8), objects=[])
        self.state.init_border()
        pogoist: Entity = self.state.place_object("agent", Entity, properties={"loc": (2, 2)})
        pogoist.inventory = {}
        self.state.random_place("tree", 3, PolycraftObject)
        self.state.random_place("rubber", 1, PolycraftObject)
        """

        #MEDIUM
        self.state = State(map_size=(15, 15), objects=[])
        self.state.init_border()
        pogoist: Entity = self.state.place_object("agent", Entity, properties={"loc": (2, 2)})
        pogoist.inventory = {}
        

        for i in range(6):
            if i == 0:
                continue
            self.state.place_object("bedrock", PolycraftObject, properties={"loc": (i, 9)})
        for i in range(4):
            self.state.place_object("bedrock", PolycraftObject, properties={"loc": (5, 10 + i)})
        self.state.remove_object("bedrock", (4, 9))
        self.state.place_object("door", Door, properties={"loc": (4, 9)})

        self.state.random_place("tree", 3, PolycraftObject)
        self.state.random_place("rubber", 1, PolycraftObject)

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

        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state),
            "use": Use(state=self.state),
            "craft_stick": Craft(state=self.state, recipe=recipe_dict["recipes"]["stick"]),
            "craft_plank": Craft(state=self.state, recipe=recipe_dict["recipes"]["plank"]),
            "craft_pogo_stick": Craft(state=self.state, recipe=recipe_dict["recipes"]["pogo_stick"])
        }
        

    def getSymbol(self, obj, state, canWalkOver=False, facing="NORTH"):
        if obj == "tree":
            if state == "block":
                return 'T'
            else:
                return 't'
        elif obj == "air":
            return ' '
        elif obj == "bedrock":
            return 'X'
        elif obj == "door":
            if canWalkOver == True:
                return ' '
            else:
                return 'D'
        elif obj == "rubber":
            if state == "block":
                return 'R'
            else:
                return 'r'
        elif obj == "agent":
            if facing == "NORTH":
                return '^'
            elif facing == "SOUTH":
                return 'v'
            elif facing == "EAST":
                return ">"
            else:
                return "<"
        else:
            return ' '

    def mapRepresentation(self):
        res: np.ndarray = np.empty(self.state.initial_info["map_size"], dtype="object")
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                obj = self.state.get_objects_at((i,j))
                if len(obj[0]) != 0:
                    if hasattr(obj[0][0], "canWalkOver"):
                        res[i][j] = self.getSymbol(obj[0][0].type, obj[0][0].state, canWalkOver=obj[0][0].canWalkOver)
                    else:
                        res[i][j] = self.getSymbol(obj[0][0].type, obj[0][0].state)
                else:
                    res[i][j] = ' '
                if len(obj[1]) != 0:
                    if hasattr(obj[1][0], "facing"):
                        res[i][j] = self.getSymbol(obj[1][0].type, obj[1][0].state, facing=obj[1][0].facing)
                    else:
                        res[i][j] = self.getSymbol(obj[1][0].type, obj[1][0].state)
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
                elif choice == "use":
                    self.actions["use"].do_action(agent)
                elif choice == "craft_stick":
                    self.actions["craft_stick"].do_action(agent)
                elif choice == "craft_plank":
                    self.actions["craft_plank"].do_action(agent)
                elif choice == "craft_pogo_stick":
                    self.actions["craft_pogo_stick"].do_action(agent)

def main():
    print("Goal: Craft Pogostick (1 Rubber, 2 Planks, 4 Sticks)")
    time.sleep(1)
    test = TestRender()
    test.setUp()
    test.mainLoop()

if __name__ == '__main__':
    main()