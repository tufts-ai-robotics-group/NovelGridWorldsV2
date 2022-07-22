from ..objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door
from gym_novel_gridworlds2.state.cell import Cell
from gym_novel_gridworlds2.state.exceptions import LocationOccupied

import random
import numpy as np


class PolycraftState(State):
    """
    Extended State Representation with extra helper functions
    """

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

    def init_border(self):
        """
        Initializes a bedrock border surrounding the edges of the map
        """
        for i in range(self.initial_info["map_size"][0]):
            for j in range(self.initial_info["map_size"][1]):
                if i == 0 or j == 0:
                    self.place_object("bedrock", properties={"loc": (i, j)})
                elif i == self.initial_info["map_size"][0] - 1:
                    self.place_object("bedrock", properties={"loc": (i, j)})
                elif j == self.initial_info["map_size"][1] - 1:
                    self.place_object("bedrock", properties={"loc": (i, j)})

    def init_border_multi(self, start, end):
        """
        Given a start and an endpoint,
        initializes a bedrock border surrounding the edges
        """
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

        # # for every wall, randomly init a door to replace a bedrock there
        # coord = (0, 0)
        # for wall in self.walls_list:
        #     without_borders = wall[1 : len(wall) - 1]
        #     # don't want to place a door where its inaccessible
        #     coord = tuple(self.rng.choice(without_borders))
        # properties = {"loc": coord}
        # self.remove_object("bedrock", coord)
        # self.place_object("door", Door, properties=properties)

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
        # generate a num between 4 - 7
        # that many steps later, generate a floating sapling at loc
        self.time_needed = random.randint(4, 7)
        self.loc_to_place = loc

    def time_updates(self):
        if self.time_needed > 0:
            self.time_needed -= 1
        if self.time_needed == 0:
            if (  # case where the tile where the sapling should be placed is empty
                len(self.get_objects_at(self.loc_to_place)[0]) == 0
                and len(self.get_objects_at(self.loc_to_place)[1]) == 0
            ):
                self.place_object(
                    "sapling",
                    PolycraftObject,
                    properties={"loc": self.loc_to_place, "state": "floating"},
                )
            elif (  # case where agent is on the tile where the sapling should be placed
                len(self.get_objects_at(self.loc_to_place)[1]) == 1
                and (
                    self.get_objects_at(self.loc_to_place)[1][0].type == "agent"
                    or self.get_objects_at(self.loc_to_place)[1][0].type == "pogoist"
                )
            ):
                if "sapling" in self.get_objects_at(self.loc_to_place)[1][0].inventory:
                    self.get_objects_at(self.loc_to_place)[1][0].inventory[
                        "sapling"
                    ] += 1
                else:
                    self.get_objects_at(self.loc_to_place)[1][0].inventory.update(
                        {"sapling": 1}
                    )
            else:  # case where the tile where the sapling should be placed is nonempty
                vec = None
                obj1 = self.get_objects_at(np.add(self.loc_to_place, (-1, 0)))  # north
                if len(obj1[0]) == 0 and len(obj1[1]) == 0:
                    vec = (-1, 0)
                obj2 = self.get_objects_at(np.add(self.loc_to_place, (1, 0)))  # south
                if len(obj2[0]) == 0 and len(obj2[1]) == 0:
                    vec = (1, 0)
                obj3 = self.get_objects_at(np.add(self.loc_to_place, (0, 1)))  # east
                if len(obj3[0]) == 0 and len(obj3[1]) == 0:
                    vec = (0, 1)
                obj4 = self.get_objects_at(np.add(self.loc_to_place, (0, -1)))  # west
                if len(obj4[0]) == 0 and len(obj4[1]) == 0:
                    vec = (0, -1)

                new_loc = tuple(np.add(self.loc_to_place, vec))
                self.place_object(
                    "sapling",
                    PolycraftObject,
                    properties={"loc": new_loc, "state": "floating"},
                )

            self.time_needed = -1
