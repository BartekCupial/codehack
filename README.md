# CodeHack

CodeHack is a library of code-based skills for the
[NetHack Learning Environment](https://github.com/facebookresearch/nle) and
[MiniHack](https://github.com/facebookresearch/minihack). It sits between a controller and the game environment:
the controller chooses a semantic action such as `explore_room`, `fight_melee`, `open_container_key`,
`cross_lava_river`, or `descend_stairs`, and CodeHack expands that choice into primitive NetHack commands.

Project page: [Up and Down the Abstraction Ladder](https://bartekcupial.github.io/abstraction-ladder/)
Baselines: [codehack-baselines](https://github.com/BartekCupial/codehack-baselines)

## Highlights

In the paper experiments, CodeHack skills:

- nearly triple average zero-shot NetHack progression across 14 models compared with primitive-only control,
- reduce estimated language-model inference cost per episode by 86%,
- produce a 7.2x larger average RL dungeon-level gain than primitive-only control under the same training budget,
- retain primitive fallback through mixed control, rather than forcing every decision through skills.

## Why CodeHack?

Primitive NetHack control is expressive, but it is a poor interface for long-horizon agents. Simple intentions expand
into long sequences of movement commands, menu choices, prompt responses, and recovery actions, spending language-model
calls or RL exploration on mechanics rather than decisions.

CodeHack adds a middle layer: readable Python skills that package recurring NetHack behaviors into semantic actions.
Skills such as `explore_room`, `fight_melee`, and `cross_lava_river` run cheaply, use structured game state, and return
control when they finish, fail, make no progress, or hit an unsafe state.

The goal is not to hide the primitive game. It is to let controllers move between levels of abstraction: use skills for
reusable behavior, and fall back to primitives for prompts, edge cases, and local repairs.

## Installation

Clone and install:

```bash
git clone https://github.com/BartekCupial/codehack.git
cd codehack
python -m pip install -U pip
python -m pip install .

MINOR=$(python3 -c 'import sys; print(f"cp{sys.version_info.major}{sys.version_info.minor}")')
pip install "https://github.com/BartekCupial/nle/releases/download/v1.2.1/nle-1.2.0-${MINOR}-${MINOR}-manylinux_2_17_$(uname -m).manylinux2014_$(uname -m).whl"

```

For development:

```bash
python -m pip install -e ".[dev]"

MINOR=$(python3 -c 'import sys; print(f"cp{sys.version_info.major}{sys.version_info.minor}")')
pip install "https://github.com/BartekCupial/nle/releases/download/v1.2.1/nle-1.2.0-${MINOR}-${MINOR}-manylinux_2_17_$(uname -m).manylinux2014_$(uname -m).whl"

pre-commit install
pytest
```

NLE/MiniHack installation can be platform-sensitive. If `pip install -e .` cannot resolve a compatible `nle` wheel
for your machine, install a matching NLE wheel first and then rerun the editable install.

## Quick Start

### Play With Strategies

MiniHack:

```bash
python -m codehack.envs.minihack.play_minihack \
  --env=MiniHack-Corridor-R3-v0 \
  --codehack=True \
  --strategies="['explore_corridor', 'goto_room', 'open_doors', 'fight_melee']"
```

NetHack:

```bash
python -m codehack.envs.nethack.play_nethack \
  --env=NetHackScore-v0 \
  --codehack=True \
  --strategies="['explore_room', 'explore_corridor', 'goto_unexplored_room', 'open_doors', 'fight_melee', 'pickup_food', 'eat_food_inventory', 'descend_stairs']"
```

Type `help` in the interactive prompt to list available strategy names. Tab completion is enabled for strategy
selection. By default the wrapper also exposes primitive actions such as `north`, `south`, `wait`, `more`, `pickup`,
and `zap`; pass `--primitives=False` for skill-only control.

### Step a Strategy From Python

```python
import gymnasium as gym
import minihack  # noqa: F401
from nle import nethack
from nle_utils.wrappers import AutoMore, NoProgressAbort

from codehack.bot.panics import enemy_appeared, lost_hp
from codehack.bot.strategies import explore_room, fight_melee, goto_room, open_doors
from codehack.wrappers import CodeHackWrapper, NoProgressFeedback

OBSERVATION_KEYS = (
    "message",
    "blstats",
    "tty_chars",
    "tty_colors",
    "tty_cursor",
    "glyphs",
    "inv_glyphs",
    "inv_strs",
    "inv_letters",
    "inv_oclasses",
)

env = gym.make(
    "MiniHack-Room-5x5-v0",
    observation_keys=OBSERVATION_KEYS,
    actions=nethack.ACTIONS,
)
env = AutoMore(NoProgressAbort(env))
env = CodeHackWrapper(
    env,
    strategies=[explore_room, goto_room, open_doors, fight_melee],
    panics=[enemy_appeared, lost_hp],
    primitives=["north", "south", "east", "west", "wait", "more"],
)
env = NoProgressFeedback(env)

obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step("explore_room")

print("primitive steps used:", info["episode_extra_stats"]["env_steps"])
```

`CodeHackWrapper` exposes strategy names as actions. A single `env.step("explore_room")` may consume many primitive
environment steps before returning.


### Compose Strategies in Python

The skills can also be used as building blocks inside a small Python controller. For example,
`tests/minihack/test_corridor.py` solves multiple MiniHack corridor tasks by trying navigation, door-opening,
exploration, and search skills in a simple loop:

```python
from nle_utils.play import play

from codehack.bot.exceptions import BotPanic
from codehack.bot.strategies import (
    descend_stairs,
    explore_corridor_systematically,
    explore_room,
    goto_corridor,
    goto_unexplored_room,
    open_doors_kick,
    search_corridor_for_hidden_doors,
    search_room_for_hidden_doors,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args


cfg = parse_minihack_args(
    argv=[
        "--env=MiniHack-Corridor-R3-v0",
        "--seed=0",
        "--no-render",
    ]
)


def solve_corridor(bot):
    room_searches = 0
    corridor_searches = 0

    def attempt(strategy):
        try:
            return bool(strategy(bot))
        except BotPanic:
            return False

    while True:
        for strategy in [
            descend_stairs,
            open_doors_kick,
            explore_room,
            explore_corridor_systematically,
            goto_unexplored_room,
            goto_corridor,
        ]:
            attempt(strategy)

        if bot.blstats.hunger_state < 2 and corridor_searches == 0:
            corridor_searches += 1
            attempt(search_corridor_for_hidden_doors)

        if bot.blstats.hunger_state < 2 and room_searches == 0:
            room_searches += 1
            attempt(search_room_for_hidden_doors)


cfg.strategies = [solve_corridor]
status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
assert status["end_status"].name == "TASK_SUCCESSFUL"
```

This is the pattern used throughout the MiniHack tests: compose a few reusable skills, let each skill return when it
finishes or panics, and keep the controller logic small enough to inspect.

### Write a New Skill

Strategies are ordinary Python functions decorated with `@strategy`. They receive a `Bot`, inspect structured state,
issue primitive actions through `bot.step(...)` or helpers, and return `True` when they did useful work.

```python
from codehack.bot.strategy import strategy
from codehack.bot.strategies import explore_corridor, fight_melee, open_doors


@strategy
def safe_corridor_progress(bot):
    if fight_melee(bot):
        return True

    if open_doors(bot):
        return True

    if explore_corridor(bot):
        return True

    bot.wait()
    return True
```

When adding a project skill, put it in the closest module under `codehack/bot/strategies/`, export it from
`codehack/bot/strategies/__init__.py`, and add a
focused test under `tests/strategies/`.

### Use CodeHack for RL

The native action space is a set of strings, which is convenient for language agents and scripted controllers. Most RL
libraries expect `gym.spaces.Discrete`, so wrap CodeHack with a small adapter:

```python
import gymnasium as gym


class DiscreteStrategyActions(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.strategy_names = tuple(env.action_space)
        self.action_space = gym.spaces.Discrete(len(self.strategy_names))

    def action(self, action):
        return self.strategy_names[int(action)]


env = DiscreteStrategyActions(env)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

Useful training signals:

- `obs["env_steps"]`: primitive environment steps consumed by the chosen skill.
- `obs["text_feedback"]`: no-progress feedback from `NoProgressFeedback`.
- `info["episode_extra_stats"]["strategy_reward"]`: reward accumulated inside the skill call.
- `info["episode_extra_stats"]["strategy_useful"]`: whether the selected skill changed the environment.

Use `primitives=[]` for skill-only agents, or pass primitive names such as `north`, `wait`, `pickup`, and `more` for
mixed skill/primitive control.

## MiniHack Tasks

The repository includes controlled MiniHack tasks for testing individual skills and composing them into small
controllers. The paper uses MiniHack as a diagnostic setting because it preserves NetHack mechanics while making
failures easier to interpret.

Representative task families:

- **Corridor**: procedurally generated room-and-corridor layouts that require exploration, door handling, hidden-door
  search, and staircase navigation.
- **Quest**: multi-stage tasks that combine exploration, item use, lava crossing, combat, and subgoal sequencing.
- **Combat**: melee, ranged, engulfed, diagonal, neutral-monster, and corridor-battle scenarios.
- **Item and equipment**: pickup, wear, put on, read, quaff, zap, apply, corpse, chest, and oracle tasks.
- **Terrain and puzzle mechanics**: lava crossing, ray geometry, boulder pushing, and wand-of-death style tasks.

The tests under `tests/minihack/` and `tests/strategies/` are the most useful examples of how these tasks are used as
small, reproducible checks for CodeHack behaviors.

## Code Structure

```text
src/codehack/
  wrappers/                  Gymnasium wrappers, including CodeHackWrapper and feedback wrappers.
  bot/                       Skill execution engine and structured NetHack state.
    strategies/              Navigation, combat, inventory, terrain, prompt, and puzzle skills.
    panics/                  Interrupt handlers such as lost_hp and enemy_appeared.
    inventory/               Inventory parsing, typed item objects, and item database helpers.
    pathfinder/              Movement, distance, and path-planning utilities.
    character/               Character state, role, spells, and weapon-skill parsing.
    pvp/                     Monster targeting and combat helpers.
    trap_tracker/            Trap state and trap-related utilities.
  envs/
    nethack/                 NetHack registration and interactive play entry point.
    minihack/                MiniHack registration, custom tasks, .des files, and play entry point.
  utils/                     Granularity presets, primitive actions, play helpers, and shared utilities.
  cfg/                       CLI/configuration helpers.

tests/
  strategies/                Skill-level behavior tests.
  minihack/                  Custom MiniHack environment tests.
  bot/                       State parsing and bot utility tests.
  wrappers/                  Wrapper behavior tests.
```


## Citation

If you use CodeHack, please cite the project:

```bibtex
@article{cupial2026up,
  title={Up and Down the Abstraction Ladder: Code-Based Skills for Language Agents},
  author={Cupia{\l}, Bart{\l}omiej and Tuyls, Jens and Wo{\l}czyk, Maciej and Paglieri, Davide and Klissarov, Martin and Eysenbach, Benjamin and Mi{\l}o{\'s}, Piotr and Narasimhan, Karthik R},
  journal={arXiv preprint arXiv:2609.31076},
  year={2026}
}
```
