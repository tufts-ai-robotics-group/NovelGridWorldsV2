from typing import Mapping

from ..actions import ActionSet
from .agent import Agent
from ..object import Entity
from ..utils.item_encoder import SimpleItemEncoder

class AgentRep:
    def __init__(self, action_set: ActionSet, agent: Agent, entity: Entity):
        self.action_set = action_set
        self.agent = agent
        self.entity = entity

class AgentManager:
    def __init__(self):
        self.agent_id_counter = 0
        self.agent_count = 0
        self.agents: Mapping[int, AgentRep] = {}

    def add_agent(self, action_set: ActionSet, agent: Agent, entity: Entity):
        agent_rep = AgentRep(action_set, agent, entity)
        self.agents[self.agent_id_counter] = agent_rep
        self.agent_id_counter += 1
        self.agent_count += 1
    
    def remove_agent(self, agent_id):
        self[agent_id] = None
        self.agent_count -= 1

    def get_agent(self, id: int):
        return self.agents[id]

    def do_action(self, agent_id: int, action_id: int):
        agent_entity = self.agents[agent_id].entity
        self.agents[agent_id].action_set.do_action(agent_entity, action_id)
