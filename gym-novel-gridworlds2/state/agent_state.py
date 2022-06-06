import enum
from re import S


AGENT_FACING = {
    "NORTH": 0, 
    "EAST": 1, 
    "SOUTH": 2, 
    "WEST": 3
}

class AgentState:
    def __init__(self, facing=AGENT_FACING["NORTH"], location=[0, 0], \
                inventory=[], last_actoin="", last_action_cost=0):
        self.facing = facing
        self.location = location
        self.inventory = inventory
        self.last_action = last_actoin
        self.last_action_cost = last_action_cost
