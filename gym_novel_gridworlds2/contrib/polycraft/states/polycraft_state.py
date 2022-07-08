from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

class PolycraftState(State):
    """
    Extended State Representation with extra helper functions
    """
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
        coord = (0, 0)
        for wall in self.walls_list:
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
        # # this nested for loop iterates through rows
        # for i in rows:
        #     for j in cols:
        #         if not self.contains_block((i, j)):
        #             # place bedrock until another is reached
        #             self.place_object("bedrock", properties={"loc": (i, j)})
        #         else:
        #             break
        # # this nested for loop iterates through rows backwards
        # for i in reversed(rows):
        #     for j in reversed(cols):
        #         if not self.contains_block((i, j)):
        #             # place bedrock until another is reached
        #             self.place_object("bedrock", properties={"loc": (i, j)})
        #         else:
        #             break
        # # this nested for loop iterates through cols
        # for i in rows:
        #     for j in cols:
        #         if not self.contains_block((i, j)):
        #             # place bedrock until another is reached
        #             self.place_object("bedrock", properties={"loc": (i, j)})
        #         else:
        #             break
        # # this nested for loop iterates through cols backwards
        # for i in reversed(rows):
        #     for j in reversed(cols):
        #         if not self.contains_block((i, j)):
        #             # place bedrock until another is reached
        #             self.place_object("bedrock", properties={"loc": (i, j)})
        #         else:
        #             break