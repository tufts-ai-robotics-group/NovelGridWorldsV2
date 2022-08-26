# NovelGridWorlds Version 2
This is a redesigned version of NovelGridWorlds, built on top of OpenAI gym.
The project is tested on Python 3.8, 3.9, and 3.10.

## Installation

To install the project directly from source, go to the root folder of the
project, activate your python environment (if applicable), and run

```
pip install .
```

## Running Examples
There are example files in the `examples` folder. Just
make sure you install
the package before you run the examples.

### `polycraft.py`
This file is an example environment for polycraft. 
The file comes with some config files.

`pre_novelty_diarc.json` is a basic pre-novelty environment for diarc.
`novelty_jump.json` contains an extra novelty called "jump".

To run a config file, run
```
python3 polycraft.py <config_file>
```


## Configuration Files
We designed a format of configuration file that is easy to change,
extend, and also allows extra code to be easily imported.

Please see [here](docs/config_file.md) for the format of the configuration file.

<!-- ### `test_render_with_parser`
This file allows you to type commands manually to test the render
function in text and reproduce some errors.

### `test_color_render`
This file allows you to type commands manually to test the render
function in PyGame and reproduce some errors. -->




## Project Structure
The project consists of 5 main components: state, dynamics, actions and action sets, objects and entities, and agents.

Please see [here](docs/project_structure.md) to see detailed explanation of the
project structure.


## TODO
- wild card action set
- extendable action set
- recipe-based crafting step cost
