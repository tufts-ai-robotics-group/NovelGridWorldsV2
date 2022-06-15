from gym_novel_gridworlds2.actions import Action

class Break(Action):
    def __init__(self, state: State, dynamics, location):
        self.dynamics = dynamics
        self.state = state


    def check_precondition(self, agent_entity: Entity, target_object: Object=None, **kwargs):
        """
        Checks preconditions of the break action:
        1) The agent is facing the object to break
        2) The object is breakable 
        """
        #convert the entity facing direction to coords
        direction = (0,0) 
        if agent_entity.facing = "NORTH":
        	direction = (-1,0)
        elif agent_entity.facing = "SOUTH":
        	direction = (1,0)
        elif agent_entity.facing = "EAST":
        	direction = (0,1)
        else: 
        	direction = (0,-1)

        correctDirection = False

        if (np.add(agent_entity.loc, direction) == target_object.loc):
        	correctDirection = True

        return correctDirection && (target_object.state == "block")

    def do_action(self, agent_entity: Entity, target_object: Object):
        """
        Given the agent and the target plus corresponding extra arguments,
        Do the action if the action's precondition is met.
        Raises error if the action's precondition is not met.
        """
        pass
