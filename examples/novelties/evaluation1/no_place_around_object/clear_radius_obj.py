from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftObject

RADIUS = 2
TARGET_OBJS = ["oak_log", "bedrock"]

class ClearRadiusPolycraftObject(PolycraftObject):
    @staticmethod
    def placement_reqs(map_state, loc):
        """
        The obj cannot be placed too close to a wall.
        """
        map_size = map_state.get_map_size()
        for i in range(max(0, loc[0] - RADIUS), min(map_size[0], loc[0] + RADIUS + 1)):
            for j in range(max(0, loc[1] - RADIUS), min(map_size[1], loc[1] + RADIUS + 1)):
                objs = map_state.get_objects_at((i, j))
                if len(objs[0]) > 0:
                    if objs[0][0].type in TARGET_OBJS:
                        return False
        return True
 