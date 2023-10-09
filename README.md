# Novel GridWorlds Version 2 (NovelGridWorldsV2)

This is a redesigned version of gym-novel-gridworlds, which

> are [OpenAI Gym](https://github.com/openai/gym) environments for developing and evaluating AI agents that can detect and adapt to unknown sudden novelties in their environments. In each environment, the agent needs to craft objects using multiple recipes, which requires performing certain steps in some sequence.

What is new in this version:

1. possibility of multi-agent reinforcement learning,

2. improved customisability of environment,

3. improved modularity of novelty implementation.

This project has been tested on Python 3.8, 3.9, and 3.10.

## Installation

To install this project, you can clone this repository, activate your Python environment such as `venv` or `conda` (if applicable), and install dependencies using `pip`.

```
git clone <repo_https>
cd NovelGridWorldsV2
pip install .
```

## Basic Usage

### Project Structure

The project consists of five main components, namely the state, dynamics, actions and action sets, objects and entities, and agents. See [docs/project_structure.md](docs/project_structure.md) for a detailed explanation of the project structure.

### Running Examples

In the `examples` folder, you can find the sample environment `polycraft.py`, which can be run using

```
python3 polycraft.py <config_file>
```

where the `<config_file>` is a `.yaml` file specifying the configuration of all the components of the project. For some introductory interaction with the environment through a keyboard agent, assuming that you are in the `examples` folder, run

```
python3 polycraft.py polycraft_gym_main.yaml
```

For more detail on how the project structure translates into the creation of config files for `polycraft.py`, see [docs/config_file.md](docs/config_file.md).

## Basic Novelty Injection

To see how a simple novelty can be implemented, see the `axe_to_break` folder under `examples/novelties`. This is a novelty under which the agent must hold axe initially in its inventory in order to break trees. To demonstrate this novelty, assuming that you are in the `examples` folder, run

```
python3 polycraft.py novelties/axe_to_break/axe_to_break.yaml
```

For documentation of all novelties, see [NovelGridWorldsV2 Novelty Documentation](https://docs.google.com/document/d/1jefIDrk-SWubPeo3yOMsDN8w0XeVg_CStB2Q5dY5oqM/edit?usp=sharing). For more detail on how to implement and inject your own novelties, see [docs/config_file.md](docs/config_file.md).

## NovelGym

For a continuation of the NovelGridWorldsV2 project, see NovelGym, a wrapper on this repository that

1. only uses one agent and focuses on environment development,

2. adds and modularizes agent strategies in novelty encounters,

3. demonstrates the use of different libraries such as `tianshou`.

The NovelGym repository elaborates on the connection between the NovelGridWorldsV2 project and the NovelGym project.
