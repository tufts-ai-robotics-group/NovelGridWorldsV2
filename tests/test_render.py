from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.utils.json_parser import ConfigParser

class TestRender():
    def setUp():
        self.state = State(map_size=(5, 8), objects=[])
        self.actions = {
            "up": Move(direction="UP", state=self.state),
            "down": Move(direction="DOWN", state=self.state),
            "left": Move(direction="LEFT", state=self.state),
            "right": Move(direction="RIGHT", state=self.state),
            "break": Break(state=self.state)
        }
    def mainLoop():

        obj: Entity = self.state.place_object("agent", Entity, properties={"loc": (1, 2)})