import json
import importlib
from typing import Type

from ..actions.action_set import ActionSet

from ..agents import Agent
from ..object.entity import Entity


from ..contrib.polycraft.actions.craft import Craft
from ..state import State


class ParseError(Exception):
    pass

class ConfigParser:
    def parse_json(self, state: State, json_file_name):
        self.state = state
        self.json_content = None
        with open(json_file_name, "r") as f:
            self.json_content = json.load(f)

        self.actions = {}

        # recipe
        self.parse_recipe(self.json_content['recipes'])

        # actions
        for key, action_info in self.json_content['actions'].items():
            self.actions[key] = self.create_action(action_info)
        
        # action sets
        self.action_sets = {}
        for key, action_list in self.json_content['action_sets'].items():
            self.action_sets[key] = self.create_action_set(action_list)
        
        # entities
        self.entities = {}
        for key, entity_info in self.json_content['entities'].items():
            self.entities[key] = self.create_entity(entity_info)
        
        return (self.recipe, self.actions, self.action_sets, self.entities)

    
    def parse_recipe(self, recipe_dict):
        items = list(recipe_dict.keys())
        for i in range(len(items)):
            craftStr = "craft_" + items[i]
            self.actions[craftStr] = Craft(state=self.state, recipe=recipe_dict[items[i]])


    def create_object(self, obj_infos, obj_name):
        if type(obj_info) == str:
            obj_info = {
                "module": obj_info,
                "params": {}
            }
        ObjectModule = importlib.import_module(obj_info['module'])
        return ObjectModule(name=obj_name, **obj_info['params'])


    def create_action(self, action_info):
        ActionModule = importlib.import_module(action_info['module'])
        del action_info['module']
        action = ActionModule(**action_info)
        return action

    def create_action_set(self, action_str_list):
        action_list = []
        for action_str in action_str_list:
            action_list.append(self.actions[action_str])
        return action_list

    def create_entity(self, name: str, entity_info: dict):
        AgentClass: Type[Agent] = importlib.import_module(entity_info['agent'])
        EntityClass: Type[Entity] = importlib.import_module(entity_info['entity'])

        # action set
        try:
            action_set_name = entity_info['action_set']
            action_set: ActionSet = self.action_sets[action_set_name]
        except KeyError as e:
            raise ParseError(f'Action Set {action_set_name} not found in config') from e
        
        # entity object
        info = entity_info.copy()
        del info['agent']
        del info['entity']
        del info['action_set']
        entity_obj = EntityClass(**info)

        # agent object
        agent_obj = AgentClass(name=name, action_space=action_set.get_actionset())
        return {
            "action_set": action_set,
            "agent": agent_obj,
            "entity": entity_obj
        }
