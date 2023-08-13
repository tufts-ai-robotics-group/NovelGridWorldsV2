import pathlib
import numpy as np
import time

import pygame

from gym_novel_gridworlds2.utils.json_parser import ConfigParser


class TestColorRender:
    def setUp(self):
        self.json_parser = ConfigParser()
        self.state, self.dynamic, self.entities = self.json_parser.parse_json(
            pathlib.Path(__file__).parent.resolve() / "pre_novelty.json"
        )

    def mainLoop(self):
        won = False
        while not won:
            agent = self.state.get_objects_of_type("agent")[0]
            if "pogo_stick" in agent.inventory:
                won = True
                print("You won!")
            else:
                self.state.time_updates()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.state.SCREEN.fill((171, 164, 164))
                self.state._draw_map()

                font = pygame.font.Font("freesansbold.ttf", 18)

                step_text = font.render(
                    "Step:" + str(self.state._step_count), True, (0, 0, 0)
                )
                step_rect = step_text.get_rect()
                step_rect.center = (1120, 30)
                self.state.SCREEN.blit(step_text, step_rect)

                agent = self.state.get_objects_of_type("agent")[0]

                facing_text = font.render(
                    "Agent Facing:" + str(agent.facing), True, (0, 0, 0)
                )
                facing_rect = facing_text.get_rect()
                facing_rect.center = (1120, 60)
                self.state.SCREEN.blit(facing_text, facing_rect)

                black = (0, 0, 0)
                inv_text = "Agent Inventory:" + str(agent.inventory)

                self.state.renderTextCenteredAt(
                    inv_text,
                    font,
                    black,
                    1120,
                    90,
                    self.state.SCREEN,
                    200,
                )
                pygame.display.update()
                print("")
                print(
                    "Actions: smooth_move w (sw), rotate_r (r), rotate_l (l), break (b), use (u), collect (c), select_tree_tap (st), select_iron_pickaxe (sp), place_item (pi), craft_stick (cs), craft_plank (cp), craft_tree_tap (ctt), craft_block_of_diamond (cb), craft_pogo_stick (cps), trade_block_of_platinum (tp1)"
                )
                choice = input("Select an action: ")
                if choice == "sw":
                    self.dynamic.actions["smooth_move_W"].do_action(agent)
                elif choice == "sa":
                    self.dynamic.actions["smooth_move_A"].do_action(agent)
                elif choice == "sd":
                    self.dynamic.actions["smooth_move_D"].do_action(agent)
                elif choice == "r":
                    self.dynamic.actions["rotate_right"].do_action(agent)
                elif choice == "l":
                    self.dynamic.actions["rotate_left"].do_action(agent)
                elif choice == "b":
                    self.dynamic.actions["break"].do_action(agent)
                elif choice == "u":
                    self.dynamic.actions["use"].do_action(agent)
                elif choice == "i102":
                    self.dynamic.actions["INTERACT_102"].do_action(agent)
                elif choice == "i103":
                    self.dynamic.actions["INTERACT_103"].do_action(agent)
                elif choice == "i104":
                    self.dynamic.actions["INTERACT_104"].do_action(agent)
                elif choice == "c":
                    self.dynamic.actions["collect"].do_action(agent)
                elif choice == "sr":
                    self.dynamic.actions["sense_recipes"].do_action(agent)
                elif choice == "sa":
                    self.dynamic.actions["sense_all"].do_action(agent)
                elif choice == "ss":
                    self.dynamic.actions["select_sapling"].do_action(agent)
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
                elif choice == "tp1":
                    self.dynamic.actions["trade_block_of_platinum_1"].do_action(agent)
                elif choice == "tt1":
                    self.dynamic.actions["trade_block_of_titanium_1"].do_action(agent)
                elif choice == "td1":
                    self.dynamic.actions["trade_diamond_1"].do_action(agent)
                elif choice == "tt2":
                    self.dynamic.actions["trade_block_of_titanium_2"].do_action(agent)
                elif choice == "tp2021":
                    self.dynamic.actions["TP_TO_20,17,21"].do_action(agent)
                elif choice == "tp33":
                    self.dynamic.actions["TP_TO_3,17,3"].do_action(agent)
                elif choice == "tp10":
                    self.dynamic.actions["TP_TO_1,17,0"].do_action(agent)
                elif choice == "tpe103":
                    self.dynamic.actions["TP_TO 103"].do_action(agent)


def main():
    print(
        "Goal: Craft Pogostick (1 Rubber, 2 Blocks of Diamond, 2 Blocks of Titanium, 2 Sticks)"
    )
    time.sleep(1)
    test = TestColorRender()
    test.setUp()
    test.mainLoop()


if __name__ == "__main__":
    main()
