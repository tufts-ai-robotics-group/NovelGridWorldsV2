from gym_novel_gridworlds2.contrib.polycraft.actions import Break
import numpy as np

class RandomDropBreak(Break):
    def __init__(self, random_drop_items={"oak_log": 1}, drop_prob=0.1, *args, **kwargs):
        super().__init__(**kwargs)
        self.random_drop_items = random_drop_items
        self.rng = np.random.default_rng()
        self.drop_prob = drop_prob
    
    def do_action(self, agent_entity, target_object=None, **kwargs) -> str:
        result = super().do_action(agent_entity, target_object, **kwargs)

        # random drop of a specific item
        accept_prob = self.rng.random()
        if accept_prob < self.drop_prob:
            print(f"[RandomDropBreak] prob={accept_prob}: Random drop triggered. Dropping extra items.")
            for item, count in self.random_drop_items.items():
                ObjectClass = self.dynamics.obj_types[item]["module"]
                for _ in range(count):
                    self.state.place_object(item, ObjectClass, {"state": "floating", "loc": self.temp_loc})
        else:
            print(f"[RandomDropBreak] prob={accept_prob}: Random drop not triggered. Not dropping extra items.")
        return result
