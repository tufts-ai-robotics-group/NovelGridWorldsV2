from typing import Tuple, Optional, Union
import queue

from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.agents import agent
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.object.entity import Entity, Object
import numpy as np

search_directions = {
    "EAST": np.array((0, 1)),
    "WEST": np.array((0, -1)),
    "SOUTH": np.array((1, 0)),
    "NORTH": np.array((-1, 0))
}

class Approach(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state
    
    def _in_bound(self, coord: tuple):
        shape = self.state._map.shape
        return coord[0] >= 0 and coord[1] >= 0 and \
            coord[0] < shape[0] and coord[1] < shape[1]

    def _find_nearest_obj(self, 
            start_loc: tuple, 
            desired_type: Optional[str]=None, 
            desired_obj: Optional[Object]=None, 
            distance: int=1
        ) -> Optional[Tuple[str, tuple]]:
        """
        Takes in the start location, either desired type or desired object, and
        distance.
        Does a dfs and returns the direction of the item, and its location.
        If not found, returns None.
        """

        # BFS for a path to the target object
        visited = np.zeros(self.state._map.shape, dtype=bool)
        q = queue.Queue()
        q.put(start_loc)

        while not q.empty():
            curr_loc = q.get()
            visited[curr_loc] = True
            # search if it's at the distance from the agent
            for direction, vec in search_directions.items():
                new_loc = tuple(curr_loc + vec * distance)
                if self._in_bound(new_loc) and self.state._map[new_loc] is not None:
                    if desired_type is not None and self.state._map[new_loc].type == desired_type:
                        return direction, curr_loc
                    elif desired_obj is not None and self.state._map[new_loc] == desired_obj:
                        return direction, curr_loc

            # add its adjacent blocks to the queue
            for _, vec in search_directions.items():
                new_loc = tuple(np.add(curr_loc, vec))
                if self._in_bound(new_loc) and not visited[new_loc] and self.state._map[new_loc] is None:
                    q.put(new_loc)

        # Not found, return None
        return (0, 0), None


    def _check_prepare_action(self,
        agent_entity: Entity,
        target_type: str = None,
        target_object: Object = None,
        distance: int=1,
        **kwargs
    ) -> Tuple[bool, str, tuple]:
        """
        Helper function for checking if the action is valid or not.
        Takes in all action parameters, 
        Returns if precondition met, direction of the item, and its location
        """
        if target_object is None:
            if target_type is None:
                raise TypeError("Missing target object instance or type in Approach")
            target_object_list = self.state.get_objects_of_type(target_type)
            if len(target_object_list) == 0:
                return False, None
            direction, nearest_loc = self._find_nearest_obj(agent_entity.loc, desired_type=target_type, distance=distance)
            return nearest_loc is not None, direction, nearest_loc
        else:
            raise NotImplementedError("Approach the object not implemented")


    def check_precondition(self, agent_entity: Entity, target_type: str = None, target_object: Object = None, **kwargs):
        return self._check_prepare_action(agent_entity, target_type, target_object)
    

    def do_action(self, agent_entity: Entity, target_type: str = None, target_object: Object = None, distance=1, **kwargs):
        precondition_met, direction, nearest_loc = self._check_prepare_action(
            agent_entity, 
            target_type, 
            target_object, 
            distance=distance
        )
        # print(precondition_met, direction, nearest_loc)
        # print(np.argwhere(self.state._map != None))
        if precondition_met:
            agent_entity.facing = direction
            self.state.update_object_loc(agent_entity.loc, nearest_loc)
            # print(agent_entity)

