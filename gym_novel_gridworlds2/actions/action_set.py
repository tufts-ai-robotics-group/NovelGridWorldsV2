from typing import List, Tuple
from ..object.entity import Entity
from .action import Action 
import re
from gym.spaces import Discrete

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


    def parse_command(self, command) -> int:
        """
        Given a command, returns the id of the action and its parameters
        """
        cmd_name = command.split(" ")[0].lower()
        if cmd_name not in self.action_index:
            raise KeyError(f"Command \"{command}\" not found")
        
        # get action
        action_id = self.action_index[cmd_name]
        _, action = self.actions[action_id]

        # try to parse parameters
        if hasattr(action, "cmd_format") and action.cmd_format is not None:
            match = re.match(self.action_index[cmd_name].cmd_format, command)
            if match is not None:
                # found matching parameters, do the action using the parameters
                params = match.groupdict()
                return action_id, params
        return action_id, {}


    def remove_action(self, index):
        pass

    def add_action(self, index):
        pass

    def get_action_names(self):
        return [a[0] for a in self.actions]

    def get_action_space(self):
        return Discrete(len(self.actions))
