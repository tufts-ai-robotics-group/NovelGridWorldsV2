# Config File

Config files for this project are expected to be in `.yaml` format.

The file [gym_novel_gridworlds2/utils/json_parser.py](gym_novel_gridworlds2/utils/json_parser.py) is used by the polycraft domain to populate the state.

Note that while many classes are already defined and provided in the [gym_novel_gridworlds2/contrib/polycraft] folder, you are free to create your own class files and refer to them in the same way as you would normally input a Python file. All you need to make sure is that the file is included in the Python import path.

Similarly, you can create your own version of `json_parser.py` to handle support for initialization methods specific to the domain of the project you are working on. For instance, the `json_parser.py` includes support for initializing objects in "chunks", which may not exist in your project's domain. You might also wish to write a parser for a format different from `.yaml`.

Each of the below sections elaborate on one of the keys that can be included in the `.yaml` config file.

## Actions

To add an action to the list of actions, add an entry under the `actions` key, and put the
name of the desired action as the key.

Example:
```
actions:
  break_block:
    module: gym_novel_gridworlds2.contrib.polycraft.actions.Break
    step_cost: 3600
  move_backward:
    module: gym_novel_gridworlds2.contrib.polycraft.actions.SmoothMove
    direction: X
    step_cost: 27.906975
  ...
```

| Property | Explanation |
| -------- | ------------|
| `module` | The path of the action class, which should extend the `Action` class and implement all necessary methods.|
| `action_cost` | The action cost of the action. If not specified, it defaults to 0. |
| \[extra parameters\] | Extra parameters to be passed to the constructor of the custom `Action` class.|

## Action Sets

Give a name to the action set and a provide a list of action names (as defined in the action
section) to be added to the action set.

Example:
```
action_sets:
  main:
  - use
  - collect
  - break_block
```

## Object Types

Define the class to be used to instantiate an object of a given type.

Example:
```
object_types:
  default: gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftObject
  bedrock: gym_novel_gridworlds2.contrib.polycraft.objects.UnbreakablePolycraftObject
  door: gym_novel_gridworlds2.contrib.polycraft.objects.Door
  tree_tap:
    module: gym_novel_gridworlds2.contrib.polycraft.objects.TreeTap
    collect_cost: 50000
```

Define the object type either by directly entering the module path as the value, or by using a key-value pair specifying the module path and extra parameters as needed.

## Objects

This key in the `.yaml` config file defines the number of objects of a specified type to be randomly placed in the environment. The objects will be instantiated using the defined class module in the `object_types` section of the `.yaml` config file.

If the object type named in the `objects` section is not defined under `object_types`, the parser will use the `default` module specified there. If even the `default` module is undefined, the parser will default to the `Object` class.

Note that it is possible to specify the room in which the object is to be spawned, as well as whether the objects of a given type should be "chunked", i.e. placed next to each other. Only chunks of 2 and 4 are supported.

Example:
```
objects:
  block_of_platinum:
    quantity: 4
    room: 2
    chunked: 'True'
```

## Map Size

This key defines the size of the map.

Example:
```
map_size: [16, 16]
```

## Seed

This key defines the random number generator seed of the game.

Example:
```
seed: 23
```

## Rooms

This key defines the top-left and bottom-right coordinates of the walls of a room. Bedrock will be used to generate walls and fill spaces not belonging to any room.

Example:
```
rooms:
  '2':
    start: [0, 0]
    end: [15, 15]
```

## Entities

Entities are a little more complicated than objects. They have associated action sets.

```
entities:
  main_1:
    agent: gym_novel_gridworlds2.agents.KeyboardAgent
    name: entity.polycraft.Player.name
    type: agent
    entity: gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftEntity
    action_set: main
    inventory:
      iron_pickaxe: 1
    id: 0
    room: 2
    max_step_cost: 100000
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

This key defines how the object can be crafted. Implicitly defines the `craft` action and all `craft_<recipe_name>` actions.

```
recipes:
  stick:
    input:
    - planks
    - '0'
    - planks
    - '0'
    output:
      stick: 4
    step_cost: 2400
```

The name of the recipe ("stick" in the example above) is used to create RL actions.

The input field specifies a list of input materials. The output field specifies a dictionary of objects to get if the craft action is executed. The step cost field specifies the step cost of crafting the item.

### Use in Planning Agents

For planning agents and learning agents supporting action parameters, use the predefined "craft" action and specify the list of input objects. It will look up the recipe.

### Use in Learning Agents

The json parser will automatically convert a recipe to a craft action which can be put in an action set. Simply add `craft_<recipe_name>` to the action_sets.

Example:
```
action_sets:
  main:
  - nop_placeholder1 -> select_axe
```

## Trades

Similarly to crafting, defines the inputs and outputs for a specific trade. Implicitly defines the `trade` action and all `trade_<recipe_name>` actions which can be directly used in the action sets.

Example:
```
trades:
  block_of_titanium_1:
    input:
      block_of_platinum: 1
    output:
      block_of_titanium: 1
    trader:
    - 103
```

Then, to use this trade, either use `trade` with parameters or just use `trade_block_of_titanium_1`.

## Episodes

An integer specifying the total number of episodes.

Example:

```
num_episodes: 10
```

## Extends

Extends another file, apply the "patches" from the current file to the file it's extending.

The patches are done according to RFC7386:
- if the same key exists in the new file, does a recursive update.
- if the same key exists and have value null, remove that entry from the config.

All other types of data, including strings, ints, and lists are completely overridden if the key already exists.

## Novelties

Given an episode number, apply the "patches" to the configuration file at that episode.

Example:
```
novelties:
  '0':
    entities:
      main_1:
        inventory:
          axe: 1
```

The update logic is similar to the `extends` section.