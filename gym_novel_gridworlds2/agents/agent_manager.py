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
        self.agents: Mapping[str, AgentRep] = {}

    def add_agent(self, action_set: ActionSet, agent: Agent, entity: Entity):
        agent_rep = AgentRep(action_set, agent, entity)
        self.agents["agent_" + str(self.agent_id_counter)] = agent_rep
        self.agent_id_counter += 1
        self.agent_count += 1

    # def remove_agent(self, agent_id):
    #     self[agent_id] = None
    #     self.agent_count -= 1

    def get_agent(self, id: str):
        return self.agents[id]

    def update_agent(self, id: str, state):
        self.agents[id].state = state
        print(self.agents[id].state._step_count)

    def get_possible_agents(self):
        return list(self.agents.keys())

    def get_agent_name_mapping(self):
        possible_agents = self.get_possible_agents()
        return dict(
            zip(possible_agents, [a.agent.name for _, a in self.agents.items()])
        )

    def do_action(self, agent_id: int, action_id: int):
        agent_entity = self.agents[agent_id].entity
        self.agents[agent_id].action_set.do_action(agent_entity, action_id)
