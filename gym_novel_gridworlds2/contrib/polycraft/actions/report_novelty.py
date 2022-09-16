from gym_novel_gridworlds2.object.entity import Entity
from .NOP import NOP
from gym_novel_gridworlds2.utils.game_report import get_game_time_str

class ReportNovelty(NOP):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_log_path = kwargs.get(
            "output_log_path", 
            "novelty_log_"
        ) + get_game_time_str()
    
    def do_action(self, agent_entity: Entity, target_object=None, _raw_args="", **kwargs):
        """
        Checks for precondition, then does nothing
        """
        result = super().do_action(agent_entity, target_object, _raw_args=_raw_args, **kwargs)
        with open(self.output_log_path, "a") as output_log:
            output_log.write(
                f"{self.state.episode},{self.state._step_count},{agent_entity.id},\"{_raw_args}\"\n")
        return result
