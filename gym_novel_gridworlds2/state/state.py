from tkinter import NONE
from tracemalloc import start
from typing import List, Optional, Tuple, Mapping
from copy import deepcopy
import numpy as np
import random
from functools import reduce
import json
from numpy.random import default_rng

from gym_novel_gridworlds2.object import entity

from ..object import Object, Entity
from ..utils.item_encoder import SimpleItemEncoder
from .cell import Cell
import pygame

from .exceptions import LocationOccupied, LocationOutOfBound


class State:
    def __init__(
        self,
        map_size: Tuple[int] = None,
        objects: Mapping[str, object] = None,
        map_json: dict = None,
        item_list: Mapping[str, int] = {"air": 0},
        rng: np.random.Generator = default_rng(),
        **kwargs
    ):
        """
        Initialization of the State Object.
        """
        if map_json is not None:
            if map_size is None:
                map_size = tuple(map_json.get("map").get("size"))
            if objects is None:
                objects = map_json.get("objects")

        # TODO update
        self.initial_info = {
            "map_size": map_size,
            "objects": objects,
            "item_list": item_list,
            **kwargs,
        }
        self.item_encoder = SimpleItemEncoder(item_list)

        self.walls_list = []
        # to be used to store walls where bedrock overlaps on the map

        # Initialization of the objects
        self._objects: Mapping[str, List[Object]] = {}
        self._map: np.ndarray = np.empty(map_size, dtype="object")
        self._map.fill(None)
        self.rng = rng
        self._step_count = 0
        self.time_needed = []
        self.sapling_locs = []
        self.room_coords = []
        self.entity_count = 0
        self.curr_part = 0

        self.goalAchieved = False

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
        pygame.display.set_caption("NovelGridWorlds")
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill((171, 164, 164))

    def make_copy(self):
        return deepcopy(self)

    def get_object_id(self, object_name: str):
        return self.item_encoder.get_create_id(object_name)

    def _ensure_not_none(self, loc: tuple):
        if self._map[loc] is None:
            self._map[loc] = Cell()

    def incrementer(self):
        """
        Used to update the internal state count only after all of the agents have taken their turns
        """
        self.curr_part += 1
        if self.curr_part == self.entity_count:
            self._step_count += 1
            self.curr_part = 0

    def getSymbol(self, obj, state, canWalkOver=False, facing="NORTH"):
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

    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
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

    def drawMap(self):
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

    ############################# ALL BLOCKS #############################
    def place_object(self, object_type: str, ObjectClass=Object, properties: dict = {}):
        """
        Places an object onto the map.
        Returns true if success, false if there was a block there
        """
        # get the object id for use in the object dict
        object_id = self.item_encoder.get_create_id(object_type)
        new_loc = tuple(properties["loc"])

        # sanity check
        try:
            new_loc_obj = self._map[new_loc]
        except IndexError as e:
            raise LocationOutOfBound from e

        # ensure there's a cell at this location
        self._ensure_not_none(new_loc)
        cell: Cell = self._map[new_loc]

        # instanciate object
        if "type" in properties:
            del properties["type"]
        obj = ObjectClass(object_type, **properties)

        # placing object in the map
        success = cell.place_object(obj)
        if not success:
            # map is full, skip the next step and raise an exception.
            raise LocationOccupied

        # placing object in the list
        if object_id not in self._objects:
            self._objects[object_id] = []
        self._objects[object_id].append(obj)

        return obj

    def random_place(self, object_str, count, ObjectClass=Object):
        """
        Randomly place the object in the map

        if there's not enough spots available, all available spots will be filled
        """
        all_available_spots = np.argwhere(self._map == None)
        if count >= all_available_spots.shape[0]:
            count = all_available_spots.shape[0]

        picked_indices = self.rng.choice(
            a=all_available_spots.shape[0], size=count, replace=False
        )
        for index in picked_indices:
            properties = {"loc": tuple(all_available_spots[index])}
            self.place_object(object_str, ObjectClass, properties=properties)

    def random_place_in_room(
        self, object_str, count, startPos, endPos, ObjectClass=Object
    ):
        """
        Randomly place the object in the map in a specific room

        if there's not enough spots available, all available spots will be filled
        """
        all_available_spots = []
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                if (i > startPos[0] and i < endPos[0]) and (
                    j > startPos[1] and j < endPos[1]
                ):
                    all_available_spots.append((i, j))

        picked_spots = self.rng.choice(a=all_available_spots, size=count, replace=False)

        for loc in picked_spots:
            properties = {"loc": tuple(loc)}
            self.place_object(object_str, ObjectClass, properties=properties)

    def random_place_chunk_in_room(
        self, object_str, count, startPos, endPos, ObjectClass=Object
    ):
        """
        Randomly place the object chunk in the map in a specific room

        if there's not enough spots available, all available spots will be filled
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

    def remove_object(self, object_name: str, loc: tuple):
        """
        Removes an object from the map, replacing it with air
        """
        loc = tuple(loc)
        # get the object id for use in the object dict
        object_id = self.item_encoder.get_id(object_name)
        if object_id is not None:
            # assert object_name in self._objects, f"Object {object_name} unknown."
            # won't work as object_name isnt directly comparable to objs
            # assert all(i >= j for i, j in zip(loc, [0] * self._map.ndim)), f"Location "
            obj = None

            try:
                # find the location of the object.
                obj_index = next(
                    i for i, v in enumerate(self._objects[object_id]) if v.loc == loc
                )
                obj = self._objects[object_id][obj_index]

                # remove the object from the list but without freeing.
                self._objects[object_id].pop(obj_index)

            except StopIteration:
                raise ValueError(
                    "Object "
                    + object_name
                    + " at "
                    + str(loc)
                    + " is not found in the list"
                )

            # update the map
            cell: Cell = self._map[loc]
            cell.remove_object(obj)

    def get_objects_of_type(self, object_type: str):
        """
        Gets a list of objects of specific type
        WARNING: Do not modify the locations in the object!!
        """
        type_id = self.item_encoder.get_id(object_type)
        if type_id is not None:
            return self._objects.get(type_id) or []
        else:
            return []

    def get_entity_by_id(self, entity_id: int):
        """
        Gets an entity by id
        """
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                if self._map[(i, j)] is not None:
                    if self._map[(i, j)]._contains_entity(entity_id):
                        objs = self.get_objects_at((i, j))
                        return objs[1][0]
        return None

    def get_objects_at(self, loc: tuple):
        """
        Gets all objects at a specific location.
        """
        loc = tuple(loc)
        if self._map[loc] is None:
            return ([], [])
        else:
            return self._map[loc].get_obj_entities()

    def get_object_at(self, loc: tuple):
        """
        LEGACY API:
        Gets an object at a specific location.
            If there are multiple objects, the first non-entity
            object will be returned.
        Returns None if it's not found.

        WARNING: Do not modify the locations
        """
        loc = tuple(loc)
        if self._map[loc] is None:
            return None
        objs = self._map[loc].get_obj_entities()
        if len(objs[0]) > 0:
            return objs[0][0]
        elif len(objs[1]) > 0:
            return objs[1][0]
        return None

    def update_object_loc(self, old_loc: tuple, new_loc: tuple):
        """
        Updates the location of an object.
        #TODO: fix; maybe this should move the OBJECT at the location
        while an update_entity_loc should move the ENTITY at the location
        """
        # notes: this algorithm updates both the agent state and the state.
        old_loc = tuple(old_loc)
        new_loc = tuple(new_loc)
        curr_obj = self.get_object_at(new_loc)
        if curr_obj == None or (
            hasattr(curr_obj, "canWalkOver") and curr_obj.canWalkOver == True
        ):
            # TODO: polycraft specific
            objs = self.get_objects_at(old_loc)
            if len(objs[1]) != 0:
                temp = objs[1][0]
                self._map[old_loc].remove_object(objs[1][0])

                self._ensure_not_none(new_loc)
                self._map[new_loc].place_object(temp)
                temp.loc = new_loc
                return True
            else:
                temp = objs[0][0]
                self._map[old_loc].remove_object(objs[0][0])

                self._ensure_not_none(new_loc)
                self._map[new_loc].place_object(temp)
                temp.loc = new_loc
                return True
        else:
            return False

    def is_full(self, loc: tuple):
        if self._map[loc] is None:
            return (False, False)
        return self._map[loc].is_full()

    def contains_block(self, loc: tuple):
        if self._map[loc] is None:
            return False
        return self._map[loc]._contains_block
    
    def get_all_entities(self):
        entities = []
        for name, obj_list in self._objects.items():
            if len(obj_list) > 0 and isinstance(obj_list[0], Entity):
                entities += obj_list
        return entities
    
    def get_map_rep_in_type(self):
        """
        returns a numpy array of strings, containing the object's type
        """
        map_rep = np.zeros_like(self._map, dtype=object)
        for i in range(self._map.shape[0]):
            for j in range(self._map.shape[1]):
                cell: Cell = self._map[i][j]
                if cell is not None:
                    map_rep[i][j] = cell.get_map_rep()
                else:
                    map_rep[i][j] = "air"
        return map_rep
    
    def get_map_size(self):
        return self._map.shape
            


    def clear(self):
        """
        Removes all objects from the list and clears the map/item list
        TODO not tested
        """
        # remove all objects:
        for index, obj_id in np.ndenumerate(self._map):
            if obj_id is not None:
                obj = self.get_object_at(index)
                if obj is not None:
                    self.remove_object(obj.type, index)
        # resets item encoder
        self.item_encoder = SimpleItemEncoder()
        # old version:
        """
        TODO: UNUSABLE FOR NOW, UPDATE NEEDED
        """
        # self.__init__(*self.initial_info)
