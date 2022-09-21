from gym_novel_gridworlds2.object import Object


class Wall(Object):
    @staticmethod
    def placement_reqs(map_state, loc):
        return True
