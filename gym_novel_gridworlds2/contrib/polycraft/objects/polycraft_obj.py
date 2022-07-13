from gym_novel_gridworlds2.object import Object


class PolycraftObject(Object):
    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"

    def placement_reqs(self, map_state, loc):
        return True
