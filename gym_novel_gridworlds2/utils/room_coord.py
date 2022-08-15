import numpy as np
from copy import deepcopy

class RoomCoordIterator:
    def __init__(self, begin_coord, end_coord):
        self.begin_coord = begin_coord
        self.end_coord = end_coord
        self.curr_coord = deepcopy(begin_coord)

    def __iter__(self):
        self.curr_coord = self.begin_coord
        return self
    
    def __next__(self):
        coord = None
        if self.curr_coord[0] > self.end_coord[0]:
            raise StopIteration
        elif self.curr_coord[1] == self.end_coord[1]:
            coord = tuple(self.curr_coord)
            self.curr_coord[1] = self.begin_coord[1]
            self.curr_coord[0] += 1
        else:
            coord = tuple(self.curr_coord)
            self.curr_coord[1] += 1
        return coord


class RoomCoordMeta:
    def __iter__(self):
        return RoomCoordIterator(self.begin_coord, self.end_coord)


class RoomCoord:
    __metaclass__ = RoomCoordMeta
    def __init__(self, begin_coord, end_coord):
        """
        Initializes a room set, inclusive of begin coord and end coord
        """
        self.begin_coord = begin_coord
        self.end_coord = end_coord
    
    def __contains__(self, coord: tuple):
        return np.all(self.begin_coord <= np.array(coord)) and \
               np.all(self.end_coord >= np.array(coord))
    
    def __iter__(self):
        return RoomCoordIterator(self.begin_coord, self.end_coord)

