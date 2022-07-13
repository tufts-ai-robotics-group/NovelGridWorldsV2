import pathlib
from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

import numpy as np
import time

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.forward import Forward
from gym_novel_gridworlds2.contrib.polycraft.actions.rotate_right import RotateRight
from gym_novel_gridworlds2.contrib.polycraft.actions.rotate_left import RotateLeft
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.contrib.polycraft.actions.use import Use
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import (
    PolycraftObject,
)

from gym_novel_gridworlds2.utils.json_parser import ConfigParser


class TestRenderWithParser:
    def setUp(self):
        self.json_parser = ConfigParser()
        self.state, self.dynamic, self.entities = self.json_parser.parse_json(
            pathlib.Path(__file__).parent.resolve() / "automaptest.json"
        )
        # tests/automaptest.json

    def getSymbol(self, obj, state, canWalkOver=False, facing="NORTH"):
        if obj == "tree":
            if state == "block":
                return "T"
            else:
                return "t"
        elif obj == "air":
            return " "
        elif obj == "bedrock":
            return "X"
        elif obj == "door":
            if canWalkOver == False:
                if state == "block":
                    return "D"
                else:
                    return "d"
            else:
                return " "
        elif obj == "rubber":
            if state == "block":
                return "R"
            else:
                return "r"
        elif obj == "chest":
            if state == "block":
                return "C"
            else:
                return "c"
        elif obj == "tree_tap":
            if state == "block":
                return "R"
            else:
                return "r"
        elif obj == "trader":
            if facing == "NORTH":
                return "^"
            elif facing == "SOUTH":
                return "v"
            elif facing == "EAST":
                return ">"
            else:
                return "<"
        elif obj == "agent":
            if facing == "NORTH":
                return "^"
            elif facing == "SOUTH":
                return "v"
            elif facing == "EAST":
                return ">"
            else:
                return "<"
        else:
            return " "

    def mapRepresentation(self):
        res: np.ndarray = np.empty(self.state.initial_info["map_size"], dtype="object")
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                obj = self.state.get_objects_at((i, j))
                if len(obj[0]) != 0:
                    if hasattr(obj[0][0], "canWalkOver"):
                        res[i][j] = self.getSymbol(
                            obj[0][0].type,
                            obj[0][0].state,
                            canWalkOver=obj[0][0].canWalkOver,
                        )
                    else:
                        res[i][j] = self.getSymbol(obj[0][0].type, obj[0][0].state)
                else:
                    res[i][j] = " "
                if len(obj[1]) != 0:
                    if hasattr(obj[1][0], "facing"):
                        res[i][j] = self.getSymbol(
                            obj[1][0].type, obj[1][0].state, facing=obj[1][0].facing
                        )
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
                print("Selected Item:")
                print(agent.selectedItem)
                print("")
                print(
                    "Actions: forward (f), rotate_r (r), rotate_l (l), break (b), use (u), select_tree (si), place_item (pi), craft_stick, craft_plank, craft_pogo_stick"
                )
                choice = input("Select an action: ")
                if choice == "f":
                    self.dynamic.actions["forward"].do_action(agent)
                elif choice == "r":
                    self.dynamic.actions["rotate_right"].do_action(agent)
                elif choice == "l":
                    self.dynamic.actions["rotate_left"].do_action(agent)
                elif choice == "b":
                    self.dynamic.actions["break"].do_action(agent)
                elif choice == "u":
                    self.dynamic.actions["use"].do_action(agent)
                elif choice == "si":
                    self.dynamic.actions["select_tree"].do_action(agent)
                elif choice == "pi":
                    self.dynamic.actions["place_item"].do_action(agent)
                elif choice == "craft_stick":
                    self.dynamic.actions["craft_stick"].do_action(agent)
                elif choice == "craft_plank":
                    self.dynamic.actions["craft_plank"].do_action(agent)
                elif choice == "craft_pogo_stick":
                    self.dynamic.actions["craft_pogo_stick"].do_action(agent)


def main():
    print("Goal: Craft Pogostick (1 Rubber, 2 Planks, 4 Sticks)")
    time.sleep(1)
    test = TestRenderWithParser()
    test.setUp()
    test.mainLoop()


if __name__ == "__main__":
    main()
