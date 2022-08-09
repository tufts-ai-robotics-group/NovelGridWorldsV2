from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.actions import Action, PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity, Object

import numpy as np


class Use(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_precondition(
        self, agent_entity: Entity, target_object: Object = None, **kwargs
    ):
        """
        Checks preconditions of the Use action:
        1) The agent is facing the object
        2) The object is of a valid type
        3) The object is in block state
        """
        # convert the entity facing direction to coords
        direction = (0, 0)
        if agent_entity.facing == "NORTH":
            direction = (-1, 0)
        elif agent_entity.facing == "SOUTH":
            direction = (1, 0)
        elif agent_entity.facing == "EAST":
            direction = (0, 1)
        else:
            direction = (0, -1)

        correctDirection = False

        self.temp_loc = tuple(np.add(agent_entity.loc, direction))
        objs = self.state.get_objects_at(self.temp_loc)
        if len(objs[0]) == 1:
            correctDirection = True

        validTypes = ["door", "chest", "safe", "tree_tap"]

        return (
            correctDirection
            and (objs[0][0].type in validTypes)
            and (objs[0][0].state == "block")
        )

    def do_action(self, agent_entity: Entity, target_object: Object = None, **kwargs):
        """
        Checks for precondition, then uses the object
        """
        # self.state._step_count += 1
        self.state.incrementer()
        if not self.check_precondition(agent_entity, target_object):
            self.result = "FAILED"
            self.action_metadata(agent_entity, target_object)
            obj_type = (
                target_object.type
                if hasattr(target_object, "type")
                else target_object.__class__.__name__
            )
            raise PreconditionNotMetError(
                f'Agent "{agent_entity.name}" cannot perform use on {obj_type}.'
            )
        objs = self.state.get_objects_at(self.temp_loc)
        objs[0][0].acted_upon("use", agent_entity)

        self.result = "SUCCESS"
        return self.action_metadata(agent_entity, target_object)

    def action_metadata(self, agent_entity, target_type=None, target_object=None):
        return "".join(
            "b'{“goal”: {“goalType”: “ITEM”, “goalAchieved”: '"
            + str(self.state.goalAchieved)
            + ",“Distribution”: “Uninformed”}, \
            “command_result”: {“command”: “use”, “argument”: “”, “result”: "
            + self.result
            + ", \
            “message”: “”, “stepCost: 50000}, “step”: "
            + str(self.state._step_count)
            + ", “gameOver”:false}"
        )
