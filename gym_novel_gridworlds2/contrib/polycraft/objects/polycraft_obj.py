from gym_novel_gridworlds2.object import Object

class PolycraftObject(Object):
    def acted_upon(self, action_name, agent):
        if action_name == "break":
        	self.state = "floating"
