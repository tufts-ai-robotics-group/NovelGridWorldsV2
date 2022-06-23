import json
import importlib
from typing import Type

from ..agents import Agent
from ..object.entity import Entity

from gym_novel_gridworlds2.contrib.polycraft.actions.craft import Craft
from gym_novel_gridworlds2.state import State

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
        # for key, action_info in self.json_content['actions'].items():
        #     self.actions[key] = self.create_action(action_info)
        
        # # action sets
        # self.action_sets = {}
        # for key, action_list in self.json_content['action_sets'].items():
        #     self.action_sets[key] = self.create_action_set(action_list)
        
        # # entities
        # entities = {}
        # for key, entity_info in self.json_content['entities'].items():
        #     # entities[key] = 
        #     pass

        return self.actions
    
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

    def create_entity(self, action_sets, entity_info):
        AgentClass: Type[Agent] = importlib.import_module(entity_info['agent'])
        EntityClass: Type[Entity] = importlib.import_module(entity_info['entity'])
        info = {**entity_info}
        del info['agent']
        del info['entity']
        del info['action_set']

        inventory = {}
        for name, count in entity_info['inventory'].items():
            inventory[name] = []
            for _ in range(count):
                inventory[name].append(self.create_object(name, ))

        info['inventory'] = inventory

        entity_obj = EntityClass(**info)
