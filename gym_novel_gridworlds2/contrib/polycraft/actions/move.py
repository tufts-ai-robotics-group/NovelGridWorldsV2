from gym_novel_gridworlds2.actions import Action

class Move(Action):
    def __init__(self, direction):
        if direction == "UP":
            self.vec = (-1, 0)
        elif direction == "DOWN":
            self.vec = (1, 0)
        elif direction == "LEFT":
            self.vec = (0, 1)
        else:
            self.vec = (0, -1)
    
    def check_precondition(self, dynamics, state):
        # check if it will collide, check if it's inside the map TODO
        pass
    
    def do_action(self, dynamics, state):
        # TODO fixme
        pass
