# NovelGridWorlds Version 2
This is a redesigned version of NovelGridWorlds, built on top of OpenAI gym.
The project is tested on Python 3.8, 3.9, and 3.10.

## Building

To build the project, run 
```
python3 -m build
```

## Installation

To install the project directly from source, first make sure the dependencies
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
The file comes with some config files.

`pre_novelty.json` is a basic environment pre-novelty.
`novelty_jump.json` contains an extra novelty called "jump".

To run the example, run
```
python3 polycraft.py <config_file>
```
Some example Config files:
TODO@!!!!

<!-- ### `test_render_with_parser`
This file allows you to type commands manually to test the render
function in text and reproduce some errors.

### `test_color_render`
This file allows you to type commands manually to test the render
function in PyGame and reproduce some errors. -->


## Configuration File
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

### Actions
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


### Action Sets
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
Defines the random number generator seed of the game.

### Rooms
Defines the top-left and bottom-right coordinates of the wall of a room.
Bedrock will be used to generate the walls and fill in spaces not belonging
to a room.

### Objects
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

### Entities
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

### Recipes
Defines how the object can be crafted. Automatically converted to a craft action which can be put in an action set.

Example:
```
"stick": {
    "input": [
        {
            "planks": 2
        }
    ],
    "output": [
        {
            "stick": 4
        }
    ]
},
```

```
 "action_sets": {
    "main": [
      "forward",
      "smoothmove",
      "use",
      "break",
      "craft_stick" #can input this without importing the module
    ]
  }
```

### Trades
In a very similar vein to crafting, defines the inputs and outputs for a specific trade. Automatically converted to a trade action which can be put in an action set.

Example:
```
"block_of_titanium_1": {
      "input": [
        {
          "block_of_platinum": 1
        }
      ],
      "output": [
        {
          "block_of_titanium": 1
        }
      ]
    }
```

```
 "action_sets": {
    "main": [
      "smoothmove",
      "smoothturn",
      "use",
      "break",
      "trade_block_of_titanium_1" #can input this without importing the module
    ]
  }
```

### Episodes
An integer specifying the total number of episodes.

### Novelties
Given an episode number, apply the "patches" to the configuration file.

Example:
```
"novelties": {
    "episode_number": {
        <new_content>
    }
}
```
Objects (dicts) are updated on a key-by-key basis. (i.e. if a 
key already exists, it does a recursive update. if it doesn't exist,
a new entry will be added.)

All other types of 
data, including strings, ints, and lists are completely overridden
if the key already exists.

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
The `Action` class specifies the preconditions and consequences of an 
action, depending on the type of the entity that's executing the action
and the object that is acted upon.

#### ActionSet
The `ActionSet` class represents a set of actions. Action Sets can be used to 
specify what actions are available to a specific type of entity.

### Example Agents
The project provides some generic agent that can achieve simple
tasks or serve as an example for more complicated agents:

#### `RandomAgent`
The agent will pick a random action (without parameters).

#### `KeyboardAgent`
The agent will print its action set and prompt for the user to 
manually select an action from the list.

#### `SocketAgent`
The process is basically the same as the `KeyboardAgent`, but it sends
the available actions over the socket and expects an action number to 
be send from the remote client.

To test the socket, first run the main `examples/polycraft.py` using
configuration `pre_novelty_socket.json`.
Then, go to `tests/test_socket.py` to directly send text over the socket.

If you want to test your own configuration file with a different socket
number,
make sure you change the `PORT` variable in the `test_socket.py` file to reflect
the port you're using.

## Rendering

### `General`

As rendering is entirely dependent on the images you select and how you envision your environment, we leave it up to you. For the polycraft example, rendering is available in both PyGame and as simple text in the Terminal, and provides a template as to how you can implement rendering based on the degree of complexity you need as well as the basics of how it interacts with a state and the OpenAI gym library.

```
def render(self, mode="human"):
    #this is a part of the OpenAI gym suite, implement it in your environment definition file 
    (which in polycraft is sequential.py)
```

### `Polycraft Rendering`

To add new items to render, first add the img you want to use to represent the objects. Copy the below code snippet and modify it to include the .png you are using, as well as changing the names:

```
self.OAK_LOG_IMAGE = pygame.image.load("img/polycraft/oaklog.png")
self.OAK_LOG = pygame.transform.scale(self.OAK_LOG_IMAGE, (20, 20))

self.OAK_LOG_PICKUP_IMAGE = pygame.image.load("img/polycraft/oaklogpickup.png")
self.OAK_LOG_PICKUP = pygame.transform.scale(
    self.OAK_LOG_PICKUP_IMAGE, (20, 20)
)
```
Then, modify the drawMap function in polycraft_state.py. Copy and paste the below code snippet and add it to the if/else chain, modifying to include the image you want to include and the possible states the object has:

```
elif obj[0][0].type == "oak_log":
    if obj[0][0].state == "block":
        #draws the image of the object on the tile
        self.SCREEN.blit(
            self.OAK_LOG,
            (
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
            ),
    )
    else:
        #fill the tile with white to reset it
        pygame.draw.rect(
            self.SCREEN,
            (255, 255, 255),
            [
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                self.WIDTH,
                self.HEIGHT,
            ],
        )
        #now, draw the image of the pickup on the tile
        self.SCREEN.blit(
            self.OAK_LOG_PICKUP,
            (
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
            ),
        )

```


## TODO
- a socket client
- novelty in configuration file
- Action name (currently, all actions are just instances of a class and is merely assigned an id)
- placeable or not
- done is true, quit
- reward
- Same id after we added something to the set
- wild card action set
