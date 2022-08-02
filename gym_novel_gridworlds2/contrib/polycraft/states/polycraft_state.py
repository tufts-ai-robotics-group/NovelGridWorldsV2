from gym_novel_gridworlds2.object.object import Object
from ..objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.state.cell import Cell
from gym_novel_gridworlds2.state.exceptions import LocationOccupied
from typing import List, Optional, Tuple, Mapping
from numpy.random import default_rng

import random
import numpy as np
import pygame


class PolycraftState(State):
    """
    Extended State Representation with extra helper functions
    """

    def __init__(
        self,
        map_size: Tuple[int] = None,
        objects: Mapping[str, object] = None,
        map_json: dict = None,
        item_list: Mapping[str, int] = {"air": 0},
        rng: np.random.Generator = default_rng(),
        **kwargs
    ):
        super().__init__(map_size, objects, map_json, item_list, rng, **kwargs)

        self.time_needed = (
            []
        )  # how much time is left before respective saplings spawn in their locs
        self.sapling_locs = (
            []
        )  # used to keep track of where saplings should be placed later
        self.walls_list = []  # used to store walls where bedrock overlaps on the map

        self.WIDTH = 20
        self.HEIGHT = 20
        self.MARGIN = 1
        self.CHEST_IMAGE = pygame.image.load("chest.png")
        self.CHEST = pygame.transform.scale(self.CHEST_IMAGE, (20, 20))

        self.CRAFTING_TABLE_IMAGE = pygame.image.load("craftingtable.png")
        self.CRAFTING_TABLE = pygame.transform.scale(
            self.CRAFTING_TABLE_IMAGE, (20, 20)
        )

        self.CRAFTING_TABLE_PICKUP_IMAGE = pygame.image.load("craftingtablepickup.png")
        self.CRAFTING_TABLE_PICKUP = pygame.transform.scale(
            self.CRAFTING_TABLE_PICKUP_IMAGE, (20, 20)
        )

        self.OAK_LOG_IMAGE = pygame.image.load("oaklog.png")
        self.OAK_LOG = pygame.transform.scale(self.OAK_LOG_IMAGE, (20, 20))

        self.OAK_LOG_PICKUP_IMAGE = pygame.image.load("oaklogpickup.png")
        self.OAK_LOG_PICKUP = pygame.transform.scale(
            self.OAK_LOG_PICKUP_IMAGE, (20, 20)
        )

        self.DOOR_IMAGE = pygame.image.load("door.png")
        self.DOOR = pygame.transform.scale(self.DOOR_IMAGE, (20, 20))

        self.DOOR_OPEN_IMAGE = pygame.image.load("dooropen.png")
        self.DOOR_OPEN = pygame.transform.scale(self.DOOR_OPEN_IMAGE, (20, 20))

        self.DOOR_PICKUP_IMAGE = pygame.image.load("doorpickup.png")
        self.DOOR_PICKUP = pygame.transform.scale(self.DOOR_PICKUP_IMAGE, (20, 20))

        self.DIAMOND_ORE_IMAGE = pygame.image.load("diamond_ore.png")
        self.DIAMOND_ORE = pygame.transform.scale(self.DIAMOND_ORE_IMAGE, (20, 20))

        self.DIAMOND_PICKUP_IMAGE = pygame.image.load("diamondpickup.png")
        self.DIAMOND_PICKUP = pygame.transform.scale(
            self.DIAMOND_PICKUP_IMAGE, (20, 20)
        )

        self.AXE_IMAGE = pygame.image.load("ironaxe.png")
        self.AXE = pygame.transform.scale(self.AXE_IMAGE, (20, 20))

        self.SAPLING_IMAGE = pygame.image.load("sapling.png")
        self.SAPLING = pygame.transform.scale(self.SAPLING_IMAGE, (20, 20))

        self.SAFE_IMAGE = pygame.image.load("safe.png")
        self.SAFE = pygame.transform.scale(self.SAFE_IMAGE, (20, 20))

        self.HOPPER_IMAGE = pygame.image.load("hopper.png")
        self.HOPPER = pygame.transform.scale(self.HOPPER_IMAGE, (20, 20))

        self.PLATINUM_IMAGE = pygame.image.load("platinum.png")
        self.PLATINUM = pygame.transform.scale(self.PLATINUM_IMAGE, (20, 20))

        self.PLATINUM_PICKUP_IMAGE = pygame.image.load("platinumpickup.png")
        self.PLATINUM_PICKUP = pygame.transform.scale(
            self.PLATINUM_PICKUP_IMAGE, (20, 20)
        )

        self.AGENT_IMAGE = pygame.image.load("agent.png")
        self.AGENT = pygame.transform.rotate(
            pygame.transform.scale(self.AGENT_IMAGE, (20, 20)), 90
        )

        self.POGOIST_IMAGE = pygame.image.load("pogoist.png")
        self.POGOIST = pygame.transform.rotate(
            pygame.transform.scale(self.POGOIST_IMAGE, (20, 20)), 90
        )

        self.TRADER_IMAGE = pygame.image.load("trader.png")
        self.TRADER = pygame.transform.scale(self.TRADER_IMAGE, (20, 20))

        pygame.init()
        self.SCREEN = pygame.display.set_mode((1300, 750))
        pygame.display.set_caption("NovelGridWorlds v2")
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill((171, 164, 164))

    def drawMap(self):
        """
        The primary function used to render the map out using PyGame
        Represents every slot in the 2D np array as an image based on the
        state of the object in the slot
        """
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                obj = self.get_objects_at((i, j))
                if len(obj[0]) != 0:
                    if hasattr(obj[0][0], "canWalkOver"):
                        if (
                            obj[0][0].state == "block"
                            and obj[0][0].canWalkOver == False
                        ):
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.DOOR,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif (
                            obj[0][0].state == "block" and obj[0][0].canWalkOver == True
                        ):
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.DOOR_OPEN,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        else:
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.DOOR_PICKUP,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "plastic_chest":
                        self.SCREEN.blit(
                            self.CHEST,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "axe":
                        self.SCREEN.blit(
                            self.AXE,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "crafting_table":
                        if obj[0][0].state == "block":
                            self.SCREEN.blit(
                                self.CRAFTING_TABLE,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        else:
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.CRAFTING_TABLE_PICKUP,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "oak_log":
                        if obj[0][0].state == "block":
                            self.SCREEN.blit(
                                self.OAK_LOG,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        else:
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.OAK_LOG_PICKUP,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "diamond_ore":
                        if obj[0][0].state == "block":
                            self.SCREEN.blit(
                                self.DIAMOND_ORE,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        else:
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.DIAMOND_PICKUP,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[0][0].type == "sapling":
                        pygame.draw.rect(
                            self.SCREEN,
                            (255, 255, 255),
                            [
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                self.WIDTH,
                                self.HEIGHT,
                            ],
                        )
                        self.SCREEN.blit(
                            self.SAPLING,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "safe":
                        self.SCREEN.blit(
                            self.SAFE,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "tree_tap":
                        pygame.draw.rect(
                            self.SCREEN,
                            (255, 255, 255),
                            [
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                self.WIDTH,
                                self.HEIGHT,
                            ],
                        )
                        self.SCREEN.blit(
                            self.HOPPER,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    elif obj[0][0].type == "block_of_platinum":
                        if obj[0][0].state == "block":
                            self.SCREEN.blit(
                                self.PLATINUM,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        else:
                            pygame.draw.rect(
                                self.SCREEN,
                                (255, 255, 255),
                                [
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT,
                                ],
                            )
                            self.SCREEN.blit(
                                self.PLATINUM_PICKUP,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    else:
                        pygame.draw.rect(
                            self.SCREEN,
                            (171, 164, 164),
                            [
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                self.WIDTH,
                                self.HEIGHT,
                            ],
                        )
                else:  # air
                    pygame.draw.rect(
                        self.SCREEN,
                        (255, 255, 255),
                        [
                            (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                            (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            self.WIDTH,
                            self.HEIGHT,
                        ],
                    )
                if len(obj[1]) != 0:
                    if obj[1][0].type == "agent":
                        if obj[1][0].facing == "NORTH":
                            self.SCREEN.blit(
                                self.AGENT,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "SOUTH":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.AGENT, 180),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "EAST":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.AGENT, 270),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "WEST":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.AGENT, 90),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[1][0].type == "pogoist":
                        if obj[1][0].facing == "NORTH":
                            self.SCREEN.blit(
                                self.POGOIST,
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "SOUTH":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.POGOIST, 180),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "EAST":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.POGOIST, 270),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                        elif obj[1][0].facing == "WEST":
                            self.SCREEN.blit(
                                pygame.transform.rotate(self.POGOIST, 90),
                                (
                                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                ),
                            )
                    elif obj[1][0].type == "trader":
                        self.SCREEN.blit(
                            self.TRADER,
                            (
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                            ),
                        )
                    else:
                        pygame.draw.rect(
                            self.SCREEN,
                            (51, 0, 102),
                            [
                                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                                self.WIDTH,
                                self.HEIGHT,
                            ],
                        )

    def getSymbol(self, obj, state, canWalkOver=False, facing="NORTH"):
        """
        A helper function for the text based mapRepresentation
        """
        if obj == "oak_log":
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
        elif obj == "tree_tap":
            if state == "block":
                return "R"
            else:
                return "r"
        elif obj == "safe":
            if state == "block":
                return "S"
            else:
                return "s"
        elif obj == "plastic_chest":
            if state == "block":
                return "P"
            else:
                return "p"
        elif obj == "crafting_table":
            if state == "block":
                return "C"
            else:
                return "c"
        elif obj == "diamond_ore":
            if state == "block":
                return "O"
            else:
                return "o"
        elif obj == "trader":
            if facing == "NORTH":
                return "^"
            elif facing == "SOUTH":
                return "v"
            elif facing == "EAST":
                return ">"
            else:
                return "<"
        elif obj == "agent" or obj == "pogoist":
            if facing == "NORTH":
                return "^"
            elif facing == "SOUTH":
                return "v"
            elif facing == "EAST":
                return ">"
            else:
                return "<"
        else:
            if state == "floating":
                return obj[0].lower()
            else:
                return obj[0].upper()

    def mapRepresentation(self):
        """
        Numpy based text representation of the map, not used since
        Pygame rendering was implemented
        """
        res: np.ndarray = np.empty(self.initial_info["map_size"], dtype="object")
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                obj = self.get_objects_at((i, j))
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
        return res

    def place_object(
        self, object_type: str, ObjectClass=PolycraftObject, properties: dict = {}
    ):
        try:
            result = super().place_object(object_type, ObjectClass, properties)
            return result
        except LocationOccupied as e:
            new_loc = tuple(properties["loc"])
            cell: Cell = self._map[new_loc]
            if object_type == "door" and cell._contains_object("bedrock"):
                self.remove_object("bedrock", new_loc)
                result = super().place_object(object_type, ObjectClass, properties)
                return result
            raise LocationOccupied from e

    def random_place_chunk_in_room(
        self, object_str, count, startPos, endPos, ObjectClass=Object
    ):
        """
        Randomly place the object chunk in the map in a specific room
        if there's not enough spots available, all available spots will be filled
        NOTE: currently only works for chunks of 2 and 4
        """
        all_available_spots = []
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                if (i > startPos[0] and i < endPos[0]) and (
                    j > startPos[1] and j < endPos[1]
                ):
                    all_available_spots.append((i, j))
        self.rng.shuffle(all_available_spots)
        picked_spots = []
        if count == 2:
            # need to make it so that the spots bordering the available spots are also in the available spots list
            picked_spot = None
            vec = None
            for spot in all_available_spots:
                objs = self.get_objects_at(spot)
                if len(objs[0]) == 0 and len(objs[1]) == 0:
                    north_spot = tuple(np.add(spot, (-1, 0)))
                    obj1 = self.get_objects_at(north_spot)  # north
                    if (
                        len(obj1[0]) == 0
                        and len(obj1[1]) == 0
                        and (north_spot in all_available_spots)
                    ):
                        picked_spot = spot
                        vec = (-1, 0)
                    south_spot = tuple(np.add(spot, (1, 0)))
                    obj2 = self.get_objects_at(south_spot)  # south
                    if (
                        len(obj2[0]) == 0
                        and len(obj2[1]) == 0
                        and (south_spot in all_available_spots)
                    ):
                        picked_spot = spot
                        vec = (1, 0)
                    east_spot = tuple(np.add(spot, (0, 1)))
                    obj3 = self.get_objects_at(east_spot)  # east
                    if (
                        len(obj3[0]) == 0
                        and len(obj3[1]) == 0
                        and (east_spot in all_available_spots)
                    ):
                        picked_spot = spot
                        vec = (0, 1)
                    west_spot = tuple(np.add(spot, (0, -1)))
                    obj4 = self.get_objects_at(west_spot)  # west
                    if (
                        len(obj4[0]) == 0
                        and len(obj4[1]) == 0
                        and (west_spot in all_available_spots)
                    ):
                        picked_spot = spot
                        vec = (0, -1)

                    if picked_spot is not None:  # found the spot, terminate search
                        picked_spots = [picked_spot, tuple(np.add(picked_spot, vec))]
                        break

        elif count == 4:
            picked_spot = None
            for spot in all_available_spots:
                objs = self.get_objects_at(spot)
                if len(objs[0]) == 0 and len(objs[1]) == 0:
                    count = 0
                    south_spot = tuple(np.add(spot, (1, 0)))
                    obj1 = self.get_objects_at(south_spot)  # south
                    if (
                        len(obj1[0]) == 0
                        and len(obj1[1]) == 0
                        and south_spot in all_available_spots
                    ):
                        picked_spot = spot
                        count += 1
                    east_spot = tuple(np.add(spot, (0, 1)))
                    obj2 = self.get_objects_at(east_spot)  # east
                    if (
                        len(obj2[0]) == 0
                        and len(obj2[1]) == 0
                        and east_spot in all_available_spots
                    ):
                        picked_spot = spot
                        count += 1
                    diagonal_spot = tuple(np.add(spot, (1, 1)))
                    obj3 = self.get_objects_at(diagonal_spot)  # diagonal down
                    if (
                        len(obj3[0]) == 0
                        and len(obj3[1]) == 0
                        and diagonal_spot in all_available_spots
                    ):
                        picked_spot = spot
                        count += 1

                    if count == 3:  # we have a 2x2 chunk
                        picked_spots = [
                            picked_spot,
                            tuple(np.add(picked_spot, (1, 0))),
                            tuple(np.add(picked_spot, (0, 1))),
                            tuple(np.add(picked_spot, (1, 1))),
                        ]
                        break

        for loc in picked_spots:
            properties = {"loc": tuple(loc)}
            self.place_object(object_str, ObjectClass, properties=properties)

    def nameConversion(self, name):
        if name == None:
            return "None"
        elif name == "oak_log":
            return "minecraft:log"
        elif name == "rubber":
            return "polycraft:sack_polyisoprene_pellets"
        elif name == "block_of_titanium":
            return "polycraft:block_of_titanium"
        elif name == "block_of_platinum":
            return "polycraft:block_of_platinum"
        elif name == "diamond_ore":
            return "minecraft:diamond_ore"
        elif name == "iron_pickaxe":
            return "minecraft:iron_pickaxe"
        elif name == "block_of_diamond":
            return "minecraft:block_of_diamond"
        elif name == "tree_tap":
            return "polycraft:tree_tap"
        elif name == "plastic_chest":
            return "polycraft:plastic_chest"
        elif name == "safe":
            return "polycraft:safe"
        elif name == "bedrock":
            return "minecraft:bedrock"
        else:
            return "polycraft:" + name

    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
        """
        Resource: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font
        """
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(" ".join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = " ".join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def init_border(self, start, end):
        """
        Given a start and an endpoint,
        initializes a bedrock border surrounding the edges
        """
        coords_list = []  # need to add all the coords in the room into a list
        overlapping_wall = []
        # only one overlapping wall max, add this wall to the walls list if we place over it
        for i in range(end[0] + 1):
            for j in range(end[1] + 1):
                if i == start[0] or i == end[0] or j == start[1] or j == end[1]:
                    if i >= start[0] and j >= start[1]:
                        if not self.contains_block((i, j)):
                            self.place_object("bedrock", properties={"loc": (i, j)})
                        else:
                            overlapping_wall.append((i, j))
                if i >= start[0] and j >= start[1]:
                    coords_list.append((i, j))

        self.room_coords.append(coords_list)

        if len(overlapping_wall) > 0:
            self.walls_list.append(overlapping_wall)

        # start from every edge, place bedrock until bedrock is run into

    def init_doors(self):
        # for every wall, randomly init a door to replace a bedrock there

        for wall in self.walls_list:
            coord = (0, 0)
            without_borders = wall[1 : len(wall) - 1]
            # don't want to place a door where its inaccessible
            coord = tuple(self.rng.choice(without_borders))
            properties = {"loc": coord}
            self.remove_object("bedrock", coord)
            self.place_object("door", Door, properties=properties)

    def remove_space(self):
        # for every row, and for every col
        # proceed linearly down the row/col and place a bedrock until another bedrock is reached, then terminate
        rows = range(self.initial_info["map_size"][0])
        cols = range(self.initial_info["map_size"][1])
        # this nested for loop iterates through rows
        for i in rows:
            for j in cols:
                if not self.contains_block((i, j)):
                    # place bedrock until another is reached
                    self.place_object("bedrock", properties={"loc": (i, j)})
                else:
                    break
        # this nested for loop iterates through rows backwards
        for i in reversed(rows):
            for j in reversed(cols):
                if not self.contains_block((i, j)):
                    # place bedrock until another is reached
                    self.place_object("bedrock", properties={"loc": (i, j)})
                else:
                    break
        # this nested for loop iterates through cols
        for i in rows:
            for j in cols:
                if not self.contains_block((i, j)):
                    # place bedrock until another is reached
                    self.place_object("bedrock", properties={"loc": (i, j)})
                else:
                    break
        # this nested for loop iterates through cols backwards
        for i in reversed(rows):
            for j in reversed(cols):
                if not self.contains_block((i, j)):
                    # place bedrock until another is reached
                    self.place_object("bedrock", properties={"loc": (i, j)})
                else:
                    break

    def tree_was_broken(self, loc):
        # in 4-7 timesteps, generate a sapling at the area where the tree was broken
        self.time_needed.append(random.randint(4, 7))
        self.sapling_locs.append(loc)

    def time_updates(self):
        """
        Called after every step, updates things in the environment that elapse
        after a certain number of timesteps

        In polycraft, used to keep track of placing sapling logic after the
        elapsed timesteps
        """
        for index, time in enumerate(self.time_needed):
            if time == -1:
                continue
            if time > 0:
                self.time_needed[index] -= 1
            if time == 0:
                if (  # case where the tile where the sapling should be placed is empty
                    len(self.get_objects_at(self.sapling_locs[index])[0]) == 0
                    and len(self.get_objects_at(self.sapling_locs[index])[1]) == 0
                ):
                    self.place_object(
                        "sapling",
                        PolycraftObject,
                        properties={
                            "loc": self.sapling_locs[index],
                            "state": "floating",
                        },
                    )
                elif len(  # case where agent is on the tile where the sapling should be placed
                    self.get_objects_at(self.sapling_locs[index])[1]
                ) == 1 and (
                    self.get_objects_at(self.sapling_locs[index])[1][0].type == "agent"
                    or self.get_objects_at(self.sapling_locs[index])[1][0].type
                    == "pogoist"
                ):
                    if (
                        "sapling"
                        in self.get_objects_at(self.sapling_locs[index])[1][0].inventory
                    ):
                        self.get_objects_at(self.sapling_locs[index])[1][0].inventory[
                            "sapling"
                        ] += 1
                    else:
                        self.get_objects_at(self.sapling_locs[index])[1][
                            0
                        ].inventory.update({"sapling": 1})
                else:  # case where the tile where the sapling should be placed is nonempty
                    vec = None
                    obj1 = self.get_objects_at(
                        np.add(self.sapling_locs[index], (-1, 0))
                    )  # north
                    if len(obj1[0]) == 0 and len(obj1[1]) == 0:
                        vec = (-1, 0)
                    obj2 = self.get_objects_at(
                        np.add(self.sapling_locs[index], (1, 0))
                    )  # south
                    if len(obj2[0]) == 0 and len(obj2[1]) == 0:
                        vec = (1, 0)
                    obj3 = self.get_objects_at(
                        np.add(self.sapling_locs[index], (0, 1))
                    )  # east
                    if len(obj3[0]) == 0 and len(obj3[1]) == 0:
                        vec = (0, 1)
                    obj4 = self.get_objects_at(
                        np.add(self.sapling_locs[index], (0, -1))
                    )  # west
                    if len(obj4[0]) == 0 and len(obj4[1]) == 0:
                        vec = (0, -1)

                    new_loc = tuple(np.add(self.sapling_locs[index], vec))
                    self.place_object(
                        "sapling",
                        PolycraftObject,
                        properties={"loc": new_loc, "state": "floating"},
                    )

                self.time_needed[index] = -1
