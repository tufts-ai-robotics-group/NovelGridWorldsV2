from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np

class Use(Action):
    def __init__(self, state: State, dynamics=None):
        self.dynamics = dynamics
        self.state = state


    def check_precondition(self, agent_entity: Entity, target_object: Door=None, **kwargs):
        """
        Checks preconditions of the UseDoor action:
        1) The agent is facing the object
        2) The object is a door
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

        temp_loc = np.add(agent_entity.loc, direction)
        print(temp_loc)
        if temp_loc[0] == target_object.loc[0] and temp_loc[1] == target_object.loc[1]:
        	correctDirection = True

        return correctDirection

    def do_action(self, agent_entity: Entity, target_object: Door):
    	"""
    	Checks for precondition, then breaks the object
    	"""
    	if not self.check_precondition(agent_entity, target_object):
    		raise PreconditionNotMetError(f"Agent {agent_entity.name} cannot perform break on {target_object.type}.")
    	target_object.acted_upon("use_door", agent_entity)
    	# target_object.state = "floating"
    	# self.state.remove_object(target_object.type, target_object.loc)

