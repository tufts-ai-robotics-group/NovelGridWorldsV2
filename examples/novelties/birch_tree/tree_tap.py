from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftObject
import numpy as np


class TreeTap(PolycraftObject):
    nextToBirch = False
    def __init__(self, type="tree_tap", loc=(0, 0), state="block", **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state

    @staticmethod
    def placement_reqs(map_state, loc):
        """
        A tree must be adjacent to the spot where the tree tap is to be placed
        """
        global nextToBirch
        obj1 = map_state.get_objects_at(np.add(loc, (0, -1)))
        if len(obj1[0]) == 1:
            if obj1[0][0].type == "oak_log" and obj1[0][0].state == "block":
                return True
            if obj1[0][0].type == "birch_log" and obj1[0][0].state == "block":
                nextToBirch = True
                return True
        obj2 = map_state.get_objects_at(np.add(loc, (0, 1)))
        if len(obj2[0]) == 1:
            if obj2[0][0].type == "oak_log" and obj2[0][0].state == "block":
                return True
            if obj2[0][0].type == "birch_log" and obj2[0][0].state == "block":
                nextToBirch = True
                return True
        obj3 = map_state.get_objects_at(np.add(loc, (1, 0)))
        if len(obj3[0]) == 1:
            if obj3[0][0].type == "oak_log" and obj3[0][0].state == "block":
                return True
            if obj3[0][0].type == "birch_log" and obj3[0][0].state == "block":
                nextToBirch = True
                return True
        obj4 = map_state.get_objects_at(np.add(loc, (-1, 0)))
        if len(obj4[0]) == 1:
            if obj4[0][0].type == "oak_log" and obj4[0][0].state == "block":
                return True
            if obj4[0][0].type == "birch_log" and obj4[0][0].state == "block":
                nextToBirch = True
                return True
        return False

    def acted_upon(self, action_name, agent):
        global nextToBirch
        if action_name == "break":
            self.state = "floating"
        if action_name == "collect" and (not nextToBirch):
            if "rubber" in agent.inventory:
                agent.inventory["rubber"] += 1
            else:
                agent.inventory.update({"rubber": 1})
