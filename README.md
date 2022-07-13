# NovelGridWorlds Version 2
This is a redesigned version of NovelGridWorlds, built on top of OpenAI gym.
The project is tested on Python 3.8, 3.9, and 3.10.

## Building

To build the project, run 
```
python3 -m build
```

## Installation

To install the project directly from source, firstly make sure the dependencies
are installed by running

```
pip install -r requirements.txt
```

and then run
```
python3 setup.py install
```

## Running Examples
There are example files in the `examples` folder. Just
make sure you install
the package before you run the examples.

### `polycraft.py`
This file is an example environment for polycraft. 
The file comes with a config file called `automaptest.json`.
To run the example, run
```
python3 polycraft.py <config_file>
```

### `test_render_with_parser`
This file allows you to type commands manually to test the render
function and reproduce some errors.



## Configuration File
The included `json_parser.py` located in the `utils` folder is used by the
polycraft domain to populate the state and generate objects in the list.

Note that while many classes are predefined and provided in the `contrib/polycraft` folder,
you are free to create your own class file and refer to them
in the same way as you would normally import a python file. Just make sure
the file is included in the python import path.

### Actions
To add actions to the list, add an entry to the actions dict, and put the
name of the desired action as the key.

Example:
```
"actions": {
    "break": {
        "module": "gym_novel_gridworlds2.contrib.polycraft.actions.Break"
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
| \[extra parameters\] | Extra parameters to be passed to the constructor of the custom `Action` class.|


### Action Sets
Give a name of the action set and a list of action names (as defined in the action
section) to be added to the action set.

Example:
```
 "action_sets": {
    "main": [
      "forward",
      "rotate_left",
      "rotate_right",
      "use",
      "break"
    ],
    "trader": [
      "rotate_left",
      "rotate_right"
    ]
  }
```

### Object Types
Defines the class to be used to instantiate an object.

Example:
```
"object_types": {
    "default": "gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftObject",
    "door": "gym_novel_gridworlds2.contrib.polycraft.objects.Door",
    "tree": "gym_novel_gridworlds2.contrib.polycraft.objects.PolycraftObject"
},
```

### Map Size
Defines the size of the whole map.

### Seed
defines the random number generator seed of the game.

### Rooms
Defines the top-left and bottom-right coordinates of the wall of a room.
bedrocks will be used to generate the walls and fill in spaces not belonging
to a room.

### Objects
> Warning: currently updating api: will allow generation of object in a specific
room.

Defines the number of objects to be randomly placed in the environment.
The objects will be instatiated using the defined class module
in the `object_types` section of the json.

If the object type name is not defined in the json, the parser will
use the `default` module defined in the json. If even the `default`
module is not defined, then the parser will default to the generic, base
`Object` class.

### Entities
The situation with entities is a little more complicatedf than the objects.
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

### Recipes
Defines how the object can be crafted.

Example:
```
"stick": {
    "input": [
        {
            "plank": 2
        }
    ],
    "output": [
        {
            "stick": 4
        }
    ]
},
```

## Project Structure
The package is structured as follows:
```
gym_novel_gridworlds
├── actions
│   ├── action.py
│   └── action_set.py
├── agents
│   └── agent.py
├── contrib
│   └── polycraft
│       ├── ...
├── envs
│   └── gym_novel_gridworlds_2.py
├── object
│   ├── entity.py
│   └── object.py
├── state
│   └── state.py
└── utils
    ├── item_encoder.py
    ├── json_parser.py
    └── recipe.py
```

### Objects and Entities
The `Object` class specifies a basic model of an object.
It stores the location of an object in the world and implements basic functions that will react when it is acted upon by an entity.

The `Entity` class is a subclass of the object class. 
In addition to the properties and methods specified above, entities can also execute actions.

Extension to the objects, such as allowing the entity to have an internal inventory or specifying non-default behavior, can be achieved by creating subclasses that inherit from the base object or entity classes.


### State
The `State` class is a low-level map of the world. It allows you 
to place instances of objects on the map at specified locations. It also
allows objects to be randomly placed on empty 
spaces. Direct access to the objects placed in the map is provided through either object type or 
location.

### Action
#### Actions
The action class specifies the preconditions and consequences of an 
action, depending on the type of the entity that's executing the action
and the object that is acted upon.

#### ActionSet
The `ActionSet` class represents a set of actions. Action Sets can be used to 
specify what actions are available to a specific type of entity.


## TODO
- propagation of random seeds
- a socket client
- novelty in configuration file
- generating items in rooms
- Action name (currently, all actions are just instances of a class and is merely assigned an id)
- placeable or not
- chest with items in json
- fix place_item
