from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_entity import PolycraftEntity
from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object
from gym_novel_gridworlds2.contrib.polycraft.objects.door import Door

import numpy as np
from typing import Tuple

DIRECTIONS = [
    np.array([0, 1]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([-1, 0]),
]

def check_target(agent_entity, state: State, distance_min=1, distance_max=3) -> Tuple[bool, PolycraftEntity]:
    # checks and finds the target entity to interact with.
    agent_room = state.get_room_by_loc(agent_entity.loc)[0] # assumes the first room for easier process
    print(agent_room, distance_min, distance_max)
    for distance in range(distance_min, distance_max + 1):
        for direction in DIRECTIONS:
            tgt_loc = direction * distance + agent_entity.loc
            if tgt_loc in agent_room:
                objs = state.get_objects_at(tgt_loc)
                if len(objs[1]) == 1 and hasattr(objs[1][0], "id"):
                    return True, objs[1][0]
    return False, None


class Interact(Action):
    def __init__(self, entity_id=None, **kwargs):
        self.entity_id = entity_id
        self.cmd_format = r"\w+ (?P<entity_id>\w+)"
        super().__init__(**kwargs)

    def check_precondition(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        entity_id=None,
        **kwargs,
    ):
        """
        Checks preconditions of the Interact action:
        1) The agent is facing an entity
        2) The entity shares the id with the arg provided
        """

        # make a 3x3 radius around the agent, determine if the wanted entity is there
        if entity_id is None:
            return False
        entity_id = int(entity_id)

        can_interact, target_entity = check_target(agent_entity, self.state)
        if can_interact and target_entity.id == entity_id:
            return True
        else:
            return False

    def do_action(
        self,
        agent_entity: Entity,
        target_object: Object = None,
        entity_id=None,
        **kwargs,
    ):
        """
        Checks for precondition, then interacts with the entity
        """
        if entity_id is None:
            entity_id = self.entity_id
        
        if not self.check_precondition(
            agent_entity, target_object, entity_id=entity_id
        ):
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.nickname}" cannot interact with {entity_id}.'
            )

        _, target_object = check_target(agent_entity, self.state) #TODO optimize called twice
        target_object.acted_upon("interact", agent_entity)
        return self.action_metadata(agent_entity, target_object, entity_id=entity_id)
