from copy import deepcopy
import json
import importlib
from typing import Mapping, Tuple, Type

from gym_novel_gridworlds2.agents.agent_manager import AgentManager
from gym_novel_gridworlds2.contrib.polycraft.actions.sense_all import SenseAll
from gym_novel_gridworlds2.contrib.polycraft.states import PolycraftState

from .MultiAgentActionSpace import MultiAgentActionSpace

from ..object import Object, Entity
from ..actions import ActionSet, Action
from ..state.dynamic import Dynamic
from ..agents import Agent
import numpy as np


from ..contrib.polycraft.actions.craft import Craft
from ..contrib.polycraft.actions.select_item import SelectItem
from ..contrib.polycraft.actions.trade import Trade
from ..state import State


class ParseError(Exception):
    pass


def import_module(module_path: str):
    module_file_path, class_name = module_path.rsplit(".", 1)
    file_module = importlib.import_module(module_file_path)
    class_module = getattr(file_module, class_name)
    return class_module


class ConfigParser:
    def __init__(self) -> None:
        self.obj_types = {}
        self.agent_cache = {}

    def parse_json(
        self, json_file_name="", json_content=None
    ) -> Tuple[State, Dynamic, AgentManager]:
        """
        Parses the json, given a json content.
        TODO: check error
        """
        if json_content is None:
            with open(json_file_name, "r") as f:
                json_content = json.load(f, strict=False)
        json_content = deepcopy(json_content)

        # seed
        rng_seed = 0
        if "seed" in json_content:
            rng_seed = json_content["seed"]
        global_rng = np.random.default_rng(seed=rng_seed)

        # state
        self.state = PolycraftState(
            rng=global_rng,
            map_size=tuple(json_content["map_size"]),
        )

        # object types
        if "object_types" in json_content:
            self.parse_object_types(json_content["object_types"])

        # initialization of borders
        if "rooms" in json_content:
            for room_num, data in json_content["rooms"].items():
                self.state.init_border_multi(
                    json_content["rooms"][room_num]["start"],
                    json_content["rooms"][room_num]["end"],
                )

        # initialization of doors
        # TODO make sure all tests are passed before committing
        self.state.init_doors()

        # filling in space to prevent other objects from spawning there
        self.state.remove_space()

        # actions
        self.actions = {}
        # automatically add select_<item_name> for all items available
        select_actions = []
        for obj_type in self.obj_types:
            self.actions["select_" + obj_type] = self.create_action(
                {
                    "module": "gym_novel_gridworlds2.contrib.polycraft.actions.SelectItem",
                    "target_type": obj_type,
                }
            )
            select_actions.append("select_" + obj_type)

        # automatically add TP_TO_<coordinate> for all coordinates available on the map
        tp_to_actions = []
        for i in range(json_content["map_size"][0]):
            for j in range(json_content["map_size"][1]):
                self.actions["TP_TO_" + str(i) + ",17," + str(j)] = self.create_action(
                    {
                        "module": "gym_novel_gridworlds2.contrib.polycraft.actions.TP_TO",
                        "x": i,
                        "y": j,
                    }
                )
                tp_to_actions.append("TP_TO_" + str(i) + ",17," + str(j))

        # add manually added actions
        if "actions" in json_content:
            for key, action_info in json_content["actions"].items():
                self.actions[key] = self.create_action(action_info)

        # recipe
        if "recipes" in json_content:
            self.parse_recipe(json_content["recipes"])

        # trade
        if "trades" in json_content:
            self.parse_trades(json_content["trades"])

        # action sets
        self.action_sets = {}
        if "action_sets" in json_content:
            for key, action_list in json_content["action_sets"].items():
                self.action_sets[key] = self.create_action_set(action_list)

        # entities
        # self.entities: Mapping[str, dict] = {}
        self.agent_manager = AgentManager()
        if "entities" in json_content:
            for key, entity_info in json_content["entities"].items():
                # creates and places the entity in the map
                agent_entity = self.create_place_entity(
                    name=key, entity_info=entity_info
                )
                # add agent to the agent list (for action per round)
                self.agent_manager.add_agent(**agent_entity)

        # initializes the action space
        action_space = MultiAgentActionSpace(
            [
                e.action_set.get_action_space()
                for name, e in self.agent_manager.agents.items()
            ]
        )

        # placement of objects on the map
        if "objects" in json_content:
            for obj_name, info in json_content["objects"].items():
                if type(info["room"]) == int:
                    if info["chunked"] == "False":
                        self.create_random_obj_in_room(
                            self.state,
                            obj_name,
                            info["quantity"],
                            json_content["rooms"][str(info["room"])]["start"],
                            json_content["rooms"][str(info["room"])]["end"],
                        )
                    else:
                        self.create_obj_chunk_in_room(
                            self.state,
                            obj_name,
                            info["quantity"],
                            json_content["rooms"][str(info["room"])]["start"],
                            json_content["rooms"][str(info["room"])]["end"],
                        )
                else:
                    self.create_random_obj(self.state, obj_name, info["quantity"])

        # TODO: separate out recipes?
        dynamic = Dynamic(
            actions=self.actions,
            action_sets=self.action_sets,
            action_space=action_space,
            obj_types=self.obj_types,
        )
        return (self.state, dynamic, self.agent_manager)

    def parse_recipe(self, recipe_dict):
        items = list(recipe_dict.keys())
        for i in range(len(items)):
            craftStr = "craft_" + items[i]
            self.actions[craftStr] = Craft(
                state=self.state, recipe=recipe_dict[items[i]]
            )

        return self.actions

    def parse_trades(self, trades_dict):
        items = list(trades_dict.keys())
        for i in range(len(items)):
            tradeStr = "trade_" + items[i]
            self.actions[tradeStr] = Trade(
                state=self.state, trade=trades_dict[items[i]]
            )

        return self.actions

    def parse_object_types(self, obj_types_info: dict):
        """
        Given a dict of something like
        "default": "some_module.object_module",
        """
        self.obj_types = {}
        for key, info in obj_types_info.items():
            if type(info) == str:
                self.obj_types[key] = {"module": import_module(info), "params": {}}
            else:
                self.obj_types[key] = {
                    "module": import_module(info),
                    "params": info["params"],
                }

    def create_place_obj(self, state: State, obj_name, loc):
        """
        Given a name, creates an object using the correct name
        """
        obj_type_info = self.obj_types.get(obj_name) or self.obj_types["default"]
        ObjectModule: Object = obj_type_info["module"]
        state.place_object(
            obj_name, ObjectModule, properties={"loc": loc, **obj_type_info["params"]}
        )

    def create_random_obj(self, state: State, obj_name, quantity):
        """
        Given a name, creates an object using the correct name in a random place
        """
        obj_type_info = self.obj_types.get(obj_name) or self.obj_types["default"]
        ObjectModule: Object = obj_type_info["module"]
        state.random_place(obj_name, quantity, ObjectModule)

    def create_random_obj_in_room(
        self, state: State, obj_name, quantity, startPos, endPos
    ):
        """
        Given a name, creates an object using the correct name randomly in a given room
        """
        obj_type_info = self.obj_types.get(obj_name) or self.obj_types["default"]
        ObjectModule: Object = obj_type_info["module"]
        state.random_place_in_room(obj_name, quantity, startPos, endPos, ObjectModule)

    def create_obj_chunk_in_room(
        self, state: State, obj_name, quantity, startPos, endPos
    ):
        """
        Given a name, creates object chunk using the correct name randomly in a given room
        """
        obj_type_info = self.obj_types.get(obj_name) or self.obj_types["default"]
        ObjectModule: Object = obj_type_info["module"]
        state.random_place_chunk_in_room(
            obj_name, quantity, startPos, endPos, ObjectModule
        )

    def create_action(self, action_info):
        ActionModule: Type[Action] = import_module(action_info["module"])
        del action_info["module"]
        try:
            action = ActionModule(
                state=self.state, dynamics=self.obj_types, **action_info
            )
        except TypeError as e:
            raise ParseError(
                f"Module {ActionModule.__name__} initialization error: " + str(e)
            )
        return action

    def create_action_set(self, action_str_list):
        action_list = []
        for action_str in action_str_list:
            action_list.append((action_str, self.actions[action_str]))
        return ActionSet(action_list)

    def create_policy_agent(self, agent_info, name, entity_data, action_set):
        """
        Given agent_info,
        either reuse the existing agent and update the action_set or
        create the new agent.
        """
        if name in self.agent_cache:
            agent: Agent = self.agent_cache[name]
            agent.action_set = action_set
            agent.state = self.state
            return agent

        # import the agent class, based on two configuration styles.
        AgentClass: Type[Agent] = Agent
        agent_param = {}

        if isinstance(agent_info, str):
            # no parameter, just agent
            AgentClass = import_module(agent_info)
        else:
            AgentClass = import_module(agent_info["module"])
            agent_param = deepcopy(agent_info)
            del agent_param["module"]
        agent = AgentClass(
            name=name,
            action_set=action_set,
            state=self.state,
            entity_data=entity_data,
            **agent_param,
        )
        self.agent_cache[name] = agent
        return agent

    def create_place_entity(self, name: str, entity_info: dict):
        # import entity class
        EntityClass: Type[Entity] = import_module(entity_info["entity"])

        # action set
        try:
            action_set_name = entity_info["action_set"]
            action_set: ActionSet = self.action_sets[action_set_name]
        except KeyError as e:
            raise ParseError(f"Action Set {action_set_name} not found in config") from e

        # entity object
        entity_info["name"] = name
        entity_info["id"] = self.state.entity_count
        self.state.entity_count += 1
        entity_obj = self.state.place_object(
            entity_info["type"],
            EntityClass,
            entity_info,
        )

        # agent object
        agent_obj = self.create_policy_agent(
            entity_info["agent"],
            name=name,
            entity_data=entity_obj,
            action_set=action_set,
        )
        return {"action_set": action_set, "agent": agent_obj, "entity": entity_obj}
