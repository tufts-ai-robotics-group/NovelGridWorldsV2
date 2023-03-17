# NovelGridWorlds Version 2
This is a redesigned version of NovelGridWorlds, built on top of OpenAI gym.
The project is tested on Python 3.8, 3.9, and 3.10.

# Installation

To install the project directly from source, go to the root folder of the
project, activate your python environment (if applicable), and run

```
pip install .
```

# Running Examples
There are example files in the `examples` folder. Just
make sure you install
the package before you run the examples.

## `polycraft.py`
This file is an example environment for polycraft. 
The file comes with some config files.

- `pre_novelty_diarc.json` is a basic pre-novelty environment for diarc.
- `novelty_jump.json` contains an extra novelty called "jump".
- Other novelties are implemented 

To run a config file, run
```
python3 polycraft.py <config_file>
```

## Testing config files
To test the socket connection to diarc with config file `pre_novelty_diarc.json`
or the diarc socket connection agent,
first start NGW2 and then open a new terminal,
go to folder `tests` and run `python run_test_socket.py`.
This file serves as a dummy socket connection client.

## Phase 1 Evaluation Example Novelties
The following files are example files that may be used for evaluation. 

### Breakable Tree Taps
Tree Taps cannot be collected from anymore, but they can be broken and can yield
rubber.

file: `novelties/evaluation1/breakable_tree_taps/breakable_tree_tap.json`

### Key to Trade
Requires the agent to have a key in the inventory to trade with the trader.

file: `novelties/evaluation1/key_to_trade/key_to_trade.json`

### Convince Me.
Trees cannot be broken anymore, but you might interact with the trader
and every once in a while the trader will give you oak logs for free.

file: `novelties/evaluation1/multi_interact/multi_interact.json`

### random drop break
Trees cannot be broken anymore, but there's a chance that 
oak logs might be dropped when you break other blocks.

file: `novelties/evaluation1/random_drop_break/random_drop_break.json`

### Trees can't grow here!
You may not place saplings within 3 blocks around a tree or the wall (bedrock).

file: `novelties/evaluation1/no_place_around_object/no_place_around_object.json`

# Configuration Files
We designed a format of configuration file that is easy to change,
extend, and also allows extra code to be easily imported.

Please see [here](docs/config_file.md) for the format of the configuration file.

<!-- ## `test_render_with_parser`
This file allows you to type commands manually to test the render
function in text and reproduce some errors.

## `test_color_render`
This file allows you to type commands manually to test the render
function in PyGame and reproduce some errors. -->




# Project Structure
The project consists of 5 main components: state, dynamics, actions and action sets, objects and entities, and agents.

Please see [here](docs/project_structure.md) to see detailed explanation of the
project structure.

# Documentation of Novelties
https://docs.google.com/document/d/1jefIDrk-SWubPeo3yOMsDN8w0XeVg_CStB2Q5dY5oqM/edit?usp=sharing


# TODO
- wild card action set
- extendable action set
- recipe-based crafting step cost
- more modular rendering
