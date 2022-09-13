# Configuration File
The included `json_parser.py` located in the `utils` folder is used by the
polycraft domain to populate the state and generate objects in the list.

Note that while many classes are predefined and provided in the `contrib/polycraft` folder,
you are free to create your own class file and refer to them
in the same way as you would normally import a python file. Just make sure
the file is included in the python import path.

In a similar vein, you can create your own version of `json_parser.py` to handle support
for initialization methods that are specific to the domain of the project you are working
on specifically. For instance, the included parser includes support for initializing objects 
in chunks and in rooms, and for trades specific to the polycraft traders, which may not exist
in your project's domain.

## Actions
To add actions to the list, add an entry to the actions dict, and put the
name of the desired action as the key.

Example:
```
"actions": {
    "break": {
        "module": "gym_novel_gridworlds2.contrib.polycraft.actions.Break"
        "action_cost": 100
    },
    "name_of_other_action": {
        "module": "...",
        "extra_param1": 123,
        "extra_param2": "test",
        ...
    }
    ...
}
```

| Property | Explanation |
| -------- | ------------|
| `module` | The path of the action class, which should extend the `Action` class and implement all necessary methods.|
| `action_cost` | The action cost of the action. If not specified, it defaults to 0. |
| \[extra parameters\] | Extra parameters to be passed to the constructor of the custom `Action` class.|


## Action Sets
Give a name to the action set and a list of action names (as defined in the action
section) to be added to said action set.

Example:
```
 "action_sets": {
    "main": [
      "smoothmove",
      "smoothturn",
      "rotate_right",
      "use",
      "break"
    ],
    "trader": [
      "NOP"
    ]
  }
```

## Object Types
Defines the class to be used to instantiate an object.

Example:
```
"object_types": {
    "default": "gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftObject",
    "door": "gym_novel_gridworlds2.contrib.polycraft.objects.Door",
    "tree": "gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftObject",
    "block_of_platinum": {
        "module": "gym_novel_gridworlds2.contrib.polycraft.objects.Metal",
        "break_cost": 600
    }
}
```

Define the object type either by directly entering the module path, or using
a dictionary specifying the module path in the module key, and specifying
extra parameters as needed.

## Map Size
Defines the size of the whole map.

## Seed
Defines the random number generator seed of the game.

## Rooms
Defines the top-left and bottom-right coordinates of the wall of a room.
Bedrock will be used to generate the walls and fill in spaces not belonging
to a room.

## Objects
Defines the number of objects to be randomly placed in the environment.
The objects will be instatiated using the defined class module
in the `object_types` section of the json.

If the object type name is not defined in the json, the parser will
use the `default` module defined in the json. If even the `default`
module is not defined, then the parser will default to the generic, base
`Object` class.

In polycraft, where there are rooms and ores can be chunked,
specify the quantity of objects you want to spawn and the room in which 
they are permitted to spawn (i.e 2 if you want room 2, "Any" if you want them to
spawn in any room). Additionaly, if you set chunked to True, 
this means that all of the objects will spawn next to each other. (only 
supported for chunks of 2 and 4).

## Entities
Entities are a little more complicated than objects. They have associated action sets.
```
"main_1": {
    "agent": "gym_novel_gridworlds2.agents.RandomAgent",
    "type": "agent",
    "entity": "gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftEntity",
    "action_set": "main",
    "inventory": {
        "tree": 1
    },
    "loc": [2, 2]
},
```
| Property | Type | Explanation |
| -------- | ---- | ----------- |
| `agent` | string | The path of the agent class, which should extend the `Agent` class (in `agents/agent.py`) and implement all necessary methods.|
| `type`  | string | The type of the agent |
| `entity` | string | The path of the entity class, which should extend the `Entity` class (in `objects/entity.py`) and implement all necessary methods. |
| `action_set` | string | The action set (as defined in the action_set section) to be used |
| `inventory` | dict | the number of each type of item in the inventory. |
| `loc` | tuple | the location of the items|
| \[extra parameters\] | ... |Extra parameters to be passed to the constructor of the custom `Action` class.|

## Recipes
Defines how the object can be crafted. Implicitly defines the `craft` action
and all `craft_<recipe_name>` actions.

```
"stick": {
    "input": [
        "planks",
        "0",
        "planks",
        "0"
    ],
    "output": {
        "stick": 4
    },
    "step_cost": 2400
},
```
The name of the recipe ("stick" in the example above) is used to create
RL actions.

The input field specifies a list of input materials.
The output field specifies a dictionary of objects to get if the craft action is executed.
The step cost field specifies the step cost of crafting the item.

### Use in Planning Agents
For planning agents and learning agents supporting action
parameters, use the predefined "craft" action and specify the list of input objects. 
It will look up the recipe.


### Use in Learning Agents
The json parser will automatically 
convert a recipe to a craft action which can be put in an action set.

Simply add `craft_<recipe_name>` to the action_sets.

Example:
```
 "action_sets": {
    "main": [
      "forward",
      "smoothmove",
      "use",
      "break",
      "craft_stick" # can input this without importing the module
    ]
  }
```

## Trades
In a very similar vein to crafting, 
defines the inputs and outputs for a specific trade. 

Implicitly defines the `trade` action
and all `trade_<recipe_name>` actions which can be directly used in the action sets.

Example:
```
"block_of_titanium_1": {
    "input": {
        "block_of_platinum": 1
    },
    "output": {
        "block_of_titanium": 1
    }
}
```

Then, to use this trade, either use `trade` with parameters or just use
`trade_block_of_titanium_1`.

## Episodes
An integer specifying the total number of episodes.


## Extends
Extends another file, apply the "patches" from the current file to the
file it's extending.

The patches are done according to RFC7386:
- if the same key exists in the new file, does a recursive update.
- if the same key exists and have value null, remove that entry from the config.

All other types of 
data, including strings, ints, and lists are completely overridden
if the key already exists.


## Novelties
Given an episode number, apply the "patches" to the configuration file at that episode.

Example:
```
"novelties": {
    "episode_number": {
        <new_content>
    }
}
```
The update logic is similar to the `extends` section.
