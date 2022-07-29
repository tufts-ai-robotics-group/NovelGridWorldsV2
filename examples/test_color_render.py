import pathlib
import numpy as np
import time

import pygame

from gym_novel_gridworlds2.utils.json_parser import ConfigParser

WIDTH = 20
HEIGHT = 20
MARGIN = 1

CHEST_IMAGE = pygame.image.load("chest.png")
CHEST = pygame.transform.scale(CHEST_IMAGE, (20, 20))

CRAFTING_TABLE_IMAGE = pygame.image.load("craftingtable.png")
CRAFTING_TABLE = pygame.transform.scale(CRAFTING_TABLE_IMAGE, (20, 20))

CRAFTING_TABLE_PICKUP_IMAGE = pygame.image.load("craftingtablepickup.png")
CRAFTING_TABLE_PICKUP = pygame.transform.scale(CRAFTING_TABLE_PICKUP_IMAGE, (20, 20))

OAK_LOG_IMAGE = pygame.image.load("oaklog.png")
OAK_LOG = pygame.transform.scale(OAK_LOG_IMAGE, (20, 20))

OAK_LOG_PICKUP_IMAGE = pygame.image.load("oaklogpickup.png")
OAK_LOG_PICKUP = pygame.transform.scale(OAK_LOG_PICKUP_IMAGE, (20, 20))

DOOR_IMAGE = pygame.image.load("door.png")
DOOR = pygame.transform.scale(DOOR_IMAGE, (20, 20))

DOOR_OPEN_IMAGE = pygame.image.load("dooropen.png")
DOOR_OPEN = pygame.transform.scale(DOOR_OPEN_IMAGE, (20, 20))

DOOR_PICKUP_IMAGE = pygame.image.load("doorpickup.png")
DOOR_PICKUP = pygame.transform.scale(DOOR_PICKUP_IMAGE, (20, 20))

DIAMOND_ORE_IMAGE = pygame.image.load("diamond_ore.png")
DIAMOND_ORE = pygame.transform.scale(DIAMOND_ORE_IMAGE, (20, 20))

DIAMOND_PICKUP_IMAGE = pygame.image.load("diamondpickup.png")
DIAMOND_PICKUP = pygame.transform.scale(DIAMOND_PICKUP_IMAGE, (20, 20))

SAPLING_IMAGE = pygame.image.load("sapling.png")
SAPLING = pygame.transform.scale(SAPLING_IMAGE, (20, 20))

SAFE_IMAGE = pygame.image.load("safe.png")
SAFE = pygame.transform.scale(SAFE_IMAGE, (20, 20))

HOPPER_IMAGE = pygame.image.load("hopper.png")
HOPPER = pygame.transform.scale(HOPPER_IMAGE, (20, 20))

PLATINUM_IMAGE = pygame.image.load("platinum.png")
PLATINUM = pygame.transform.scale(PLATINUM_IMAGE, (20, 20))

PLATINUM_PICKUP_IMAGE = pygame.image.load("platinumpickup.png")
PLATINUM_PICKUP = pygame.transform.scale(PLATINUM_PICKUP_IMAGE, (20, 20))

AGENT_IMAGE = pygame.image.load("agent.png")
AGENT = pygame.transform.rotate(pygame.transform.scale(AGENT_IMAGE, (20, 20)), 90)

POGOIST_IMAGE = pygame.image.load("pogoist.png")
POGOIST = pygame.transform.rotate(pygame.transform.scale(POGOIST_IMAGE, (20, 20)), 90)

TRADER_IMAGE = pygame.image.load("trader.png")
TRADER = pygame.transform.scale(TRADER_IMAGE, (20, 20))


class TestColorRender:
    def drawMap(self):
        for i in range(self.state.initial_info["map_size"][0]):
            for j in range(self.state.initial_info["map_size"][1]):
                obj = self.state.get_objects_at((i, j))
                if len(obj[0]) != 0:
                    if hasattr(obj[0][0], "canWalkOver"):
                        if (
                            obj[0][0].state == "block"
                            and obj[0][0].canWalkOver == False
                        ):
                            SCREEN.blit(
                                DOOR,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif (
                            obj[0][0].state == "block" and obj[0][0].canWalkOver == True
                        ):
                            SCREEN.blit(
                                DOOR_OPEN,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        else:
                            SCREEN.blit(
                                DOOR_PICKUP,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "plastic_chest":
                        SCREEN.blit(
                            CHEST,
                            (
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "crafting_table":
                        if obj[0][0].state == "block":
                            SCREEN.blit(
                                CRAFTING_TABLE,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        else:
                            SCREEN.blit(
                                CRAFTING_TABLE_PICKUP,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "oak_log":
                        if obj[0][0].state == "block":
                            SCREEN.blit(
                                OAK_LOG,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        else:
                            SCREEN.blit(
                                OAK_LOG_PICKUP,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "diamond_ore":
                        if obj[0][0].state == "block":
                            SCREEN.blit(
                                DIAMOND_ORE,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        else:
                            SCREEN.blit(
                                DIAMOND_PICKUP,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "sapling":
                        SCREEN.blit(
                            SAPLING,
                            (
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "safe":
                        SCREEN.blit(
                            SAFE,
                            (
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "tree_tap":
                        SCREEN.blit(
                            HOPPER,
                            (
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "block_of_platinum":
                        if obj[0][0].state == "block":
                            SCREEN.blit(
                                PLATINUM,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        else:
                            SCREEN.blit(
                                PLATINUM_PICKUP,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    else:
                        pygame.draw.rect(
                            SCREEN,
                            (171, 164, 164),
                            [
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                                WIDTH,
                                HEIGHT,
                            ],
                        )
                else:  # air
                    pygame.draw.rect(
                        SCREEN,
                        (255, 255, 255),
                        [
                            (MARGIN + WIDTH) * j + MARGIN,
                            (MARGIN + HEIGHT) * i + MARGIN,
                            WIDTH,
                            HEIGHT,
                        ],
                    )
                if len(obj[1]) != 0:
                    if obj[1][0].type == "agent":
                        if obj[1][0].facing == "NORTH":
                            SCREEN.blit(
                                AGENT,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "SOUTH":
                            SCREEN.blit(
                                pygame.transform.rotate(AGENT, 180),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "EAST":
                            SCREEN.blit(
                                pygame.transform.rotate(AGENT, 270),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "WEST":
                            SCREEN.blit(
                                pygame.transform.rotate(AGENT, 90),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[1][0].type == "pogoist":
                        if obj[1][0].facing == "NORTH":
                            SCREEN.blit(
                                POGOIST,
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "SOUTH":
                            SCREEN.blit(
                                pygame.transform.rotate(POGOIST, 180),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "EAST":
                            SCREEN.blit(
                                pygame.transform.rotate(POGOIST, 270),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "WEST":
                            SCREEN.blit(
                                pygame.transform.rotate(POGOIST, 90),
                                (
                                    (MARGIN + WIDTH) * j + MARGIN,
                                    (MARGIN + HEIGHT) * i + MARGIN,
                                ),
                            )
                    elif obj[1][0].type == "trader":
                        SCREEN.blit(
                            TRADER,
                            (
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                            ),
                        )
                    else:
                        pygame.draw.rect(
                            SCREEN,
                            (51, 0, 102),
                            [
                                (MARGIN + WIDTH) * j + MARGIN,
                                (MARGIN + HEIGHT) * i + MARGIN,
                                WIDTH,
                                HEIGHT,
                            ],
                        )

    def setUp(self):
        self.json_parser = ConfigParser()
        self.state, self.dynamic, self.entities = self.json_parser.parse_json(
            pathlib.Path(__file__).parent.resolve() / "pre_novelty.json"
        )
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((1090, 745))
        pygame.display.set_caption("NovelGridWorlds")
        CLOCK = pygame.time.Clock()
        SCREEN.fill((171, 164, 164))

    def mainLoop(self):
        np.set_printoptions(threshold=np.inf)
        np.set_printoptions(linewidth=np.inf)

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
                self.drawMap()
                pygame.display.update()
                print("")
                print("Agent's Inventory:")
                print(agent.inventory)
                print("Selected Item:")
                print(agent.selectedItem)
                print("Agent Facing:")
                print(agent.facing)
                print("")
                print(
                    "Actions: forward (f), rotate_r (r), rotate_l (l), break (b), use (u), collect (c), select_tree_tap (st), select_iron_pickaxe (sp), place_item (pi), craft_stick (cs), craft_plank (cp), craft_tree_tap (ctt), craft_block_of_diamond (cb), craft_pogo_stick (cps), trade_block_of_platinum (tp1)"
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
                    self.dynamic.actions["TP_TO_103"].do_action(agent)


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
