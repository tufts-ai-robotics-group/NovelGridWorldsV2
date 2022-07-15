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
            pathlib.Path(__file__).parent.resolve() / "pre_novelty.json"
        )

    def mainLoop(self):
        np.set_printoptions(linewidth=np.inf)
        won = False
        while not won:
            agent = self.state.get_objects_of_type("agent")[0]
            if "pogo_stick" in agent.inventory:
                won = True
                print("You won!")
            else:
                print(self.state.mapRepresentation())
                print("")
                print("Agent's Inventory:")
                print(agent.inventory)
                print("Selected Item:")
                print(agent.selectedItem)
                print("")
                print(
                    "Actions: forward (f), rotate_r (r), rotate_l (l), break (b), use (u), extract_rubber (e), select_tree (si), select_tree_tap (st), select_iron_pickaxe (sp), place_item (pi), craft_stick (cs), craft_plank (cp), craft_tree_tap (ctt), craft_pogo_stick (cps), trade_block_of_platinum (t)"
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
                elif choice == "c":
                    self.dynamic.actions["collect"].do_action(agent)
                elif choice == "si":
                    self.dynamic.actions["select_tree"].do_action(agent)
                elif choice == "st":
                    self.dynamic.actions["select_tree_tap"].do_action(agent)
                elif choice == "sp":
                    self.dynamic.actions["select_iron_pickaxe"].do_action(agent)
                elif choice == "sc":
                    self.dynamic.actions["select_crafting_table"].do_action(agent)
                elif choice == "sb":
                    self.dynamic.actions["select_block_of_platinum"].do_action(agent)
                elif choice == "pi":
                    self.dynamic.actions["place_item"].do_action(agent)
                elif choice == "cs":
                    self.dynamic.actions["craft_stick"].do_action(agent)
                elif choice == "cp":
                    self.dynamic.actions["craft_plank"].do_action(agent)
                elif choice == "cb":
                    self.dynamic.actions["craft_block_of_diamond"].do_action(agent)
                elif choice == "ctt":
                    self.dynamic.actions["craft_tree_tap"].do_action(agent)
                elif choice == "cps":
                    self.dynamic.actions["craft_pogo_stick"].do_action(agent)
                elif choice == "t":
                    self.dynamic.actions["trade_block_of_platinum"].do_action(agent)


def main():
    print("Goal: Craft Pogostick (1 Rubber, 2 Diamond Ore, 2 Planks, 4 Sticks)")
    time.sleep(1)
    test = TestRenderWithParser()
    test.setUp()
    test.mainLoop()


if __name__ == "__main__":
    main()
