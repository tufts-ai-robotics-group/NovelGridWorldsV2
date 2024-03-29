from typing import Mapping

from ..actions import ActionSet
from .agent import Agent
from ..object import Entity
from ..utils.item_encoder import SimpleItemEncoder


class AgentRep:
    def __init__(self, action_set: ActionSet, agent: Agent, entity: Entity, max_step_cost: int):
        self.action_set = action_set
        self.agent = agent
        self.entity = entity
        self.max_step_cost = max_step_cost


class AgentManager:
    def __init__(self):
        self.agent_id_counter = 0
        self.agent_count = 0
        self.agents: Mapping[str, AgentRep] = {}

    def add_agent(self, action_set: ActionSet, agent: Agent, entity: Entity, max_step_cost: int):
        agent_rep = AgentRep(action_set, agent, entity, max_step_cost)
        self.agents["agent_" + str(agent_rep.agent.id)] = agent_rep
        self.agent_id_counter += 1
        self.agent_count += 1
    
    def get_non_env_agents(self):
        """
        returns the number of agents not environmental agents (e.g. pogoist)
        """
        active_agents = []
        for agent in self.agents.values():
            if not getattr(agent.agent, "is_env_agent", False):
                active_agents.append("agent_" + str(agent.entity.id))
        return active_agents


    # def remove_agent(self, agent_id):
    #     self[agent_id] = None
    #     self.agent_count -= 1

    def get_agent(self, id: str):
        return self.agents[id]

    def get_possible_agents(self):
        return list(self.agents.keys())

    def get_agent_name_mapping(self):
        possible_agents = self.get_possible_agents()
        return dict(
            zip(possible_agents, [a.agent.id for _, a in self.agents.items()])
        )

    def do_action(self, agent_id: int, action_id: int):
        agent_entity = self.agents[agent_id].entity
        self.agents[agent_id].action_set.do_action(agent_entity, action_id)
