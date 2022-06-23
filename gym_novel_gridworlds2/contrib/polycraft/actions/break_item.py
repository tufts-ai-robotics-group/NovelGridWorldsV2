from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np

class Break(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state


    def check_precondition(self, agent_entity: Entity, target_object: Object=None, **kwargs):
        """
        Checks preconditions of the break action:
        1) The agent is facing an object
        2) The object is breakable 
        """
        #convert the entity facing direction to coords
        direction = (0,0) 
        if agent_entity.facing == "NORTH":
            direction = (-1,0)
        elif agent_entity.facing == "SOUTH":
            direction = (1,0)
        elif agent_entity.facing == "EAST":
            direction = (0,1)
        else: 
            direction = (0,-1)

        correctDirection = False

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1:
            correctDirection = True
            if objs[0][0].type == "bedrock":
                return False
        # print(temp_loc)
        # if temp_loc[0] == target_object.loc[0] and temp_loc[1] == target_object.loc[1]:
        #     correctDirection = True

        

        return correctDirection and (objs[0][0].state == "block")

    def do_action(self, agent_entity: Entity, target_object: Object=None):
        """
        Checks for precondition, then breaks the object
        """
        if not self.check_precondition(agent_entity, target_object):
            raise PreconditionNotMetError(f"Agent {agent_entity.name} cannot perform break on {target_object.type}.")
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("break", agent_entity)
        # target_object.state = "floating"
        # self.state.remove_object(target_object.type, target_object.loc)
