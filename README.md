# NovelGridWorlds Version 2
This is a redesigned version of NovelGridWorlds, built on top of OpenAI gym.

## Installation
To build the project, run 
```
python -m build
```

To install the project directly from source, run
```
python setup.py
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
The `ActionSet` class represents a set of actions. Action Sets can be used to specify what actions are available to a specific type of entity.
