from typing import List, Mapping, Tuple, Union
from ..object.entity import Entity
from .action import Action 
import re
from gym.spaces import Discrete

class CommandParseError(Exception):
    pass

class ActionSet:
    def __init__(self, actions: List[Tuple[str, Action]]):
        self.actions = actions

        # symbolic functionalities: used to parse commands
        self.action_index = {}
        for i, (name, _) in enumerate(actions):
            self.action_index[name.lower()] = i
    
    def do_action(self, entity, index):
        action = self.actions[index][1]
        action.do_action(entity)
    
    # def parse_exec_command(self, command, entity):
    #     """
    #     Symbolic functionalities:
    #     Parse and execute a command
    #     """
    #     # fallback: no cmd_format specified and or input format not matched
    #     return action.do_action(entity)


    def parse_command(self, command: str) -> Tuple[int, Mapping[str, Union[List[str], str]]]:
        """
        Given a command, returns the id of the action and its parameters
        
        named parameters will be returned with their keys, while unnamed parameters (groups) will
        be returned as a list under the key "_all_params"
        """
        cmd_name = command.split(" ")[0].lower()
        if cmd_name not in self.action_index:
            raise CommandParseError(f"Command \"{command}\" not found")
        
        # get action
        action_id = self.action_index[cmd_name]
        _, action = self.actions[action_id]

        # try to parse parameters
        if hasattr(action, "cmd_format") and action.cmd_format is not None:
            action_index = self.action_index[cmd_name]
            match = re.match(self.actions[action_index][1].cmd_format, command, flags=re.IGNORECASE)
            if match is not None:
                # found matching parameters, do the action using the parameters
                params = match.groupdict()
                unnamed_params = match.groups()
                params["_command"] = command.split(" ")[0]
                params["_all_params"] = unnamed_params
                params["_raw_args"] = " ".join(command.split(" ")[1:])
                return action_id, params
        info = {
            "_all_params": [], 
            "_command": command.split(" ")[0], 
            "_raw_args": " ".join(command.split(" ")[1:])
        }
        return action_id, info


    def remove_action(self, index):
        pass

    def add_action(self, index):
        pass

    def get_action_names(self):
        return [a[0] for a in self.actions]

    def get_action_space(self):
        return Discrete(len(self.actions))
