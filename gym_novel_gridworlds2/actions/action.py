from ..object.entity import Entity, Object
from ..state.state import State

class PreconditionNotMetError(Exception):
    pass


class Action:
    def __init__(self, state: State, dynamics, **kwargs):
        """
        Initialize action with a reference to the state, the dynamics, and respective actions.
        """
        pass

    def check_precondition(self, agent_entity: Entity, target_type: str=None, target_object: Object=None, **kwargs):
        """
        Given the agent and the target 
        (either type of object or a reference to a specific object) 
        plus corresponding extra arguments,
        returns if the action's precondition is met.
        """
        pass

    def do_action(self, agent_entity: Entity, target_type: str=None, target_object: Object=None):
        """
        Given the agent and the target 
        (either type of object or a reference to a specific object) 
        plus corresponding extra arguments,
        Do the action if the action's precondition is met.
        Raises error if the action's precondition is not met.
        """
        pass
