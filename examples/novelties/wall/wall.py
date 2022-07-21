from gym_novel_gridworlds2.object import Object


class Wall(Object):

    def placement_reqs(self, map_state, loc):
        return True
