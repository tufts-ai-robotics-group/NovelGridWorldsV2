from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

class Move(Action):
    def __init__(self, state: State, dynamics=None, direction="UP"):
        if direction == "UP":
            self.vec = (-1, 0)
        elif direction == "DOWN":
            self.vec = (1, 0)
        elif direction == "LEFT":
            self.vec = (0, -1)
        else:
            self.vec = (0, 1)
        
        self.dynamics = dynamics
        self.state = state
    
    def check_precondition(self, agent_entity: Entity, target_type=None, target_object=None):
        """
        Checks precondition of the move action, which checks if the 
        new location is out of bound or not.
        """
        new_loc = np.add(self.vec, agent_entity.loc)
        return (new_loc >= 0).all() and \
            (new_loc < self.state._map.shape).all() and \
            self.state._map[tuple(new_loc)] is None
    

    def do_action(self, agent_entity, target_type=None, target_object=None):
        """
        Checks for precondition, then moves the object to the destination.
        """
        new_loc = tuple(np.add(self.vec, agent_entity.loc))
        if not self.check_precondition(agent_entity, target_object):
            raise PreconditionNotMetError(f"Cannot move agent {agent_entity.name} from {agent_entity.loc} to {new_loc}")
        self.state.update_object_loc(agent_entity.loc, new_loc)
