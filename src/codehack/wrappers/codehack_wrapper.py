from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import gymnasium as gym
import numpy as np
from numpy import ndarray

from codehack.bot import Bot


class StrategyActionSpace(gym.Space):
    def __init__(self, strategy_names: Iterable[str]) -> None:
        self.strategy_names = tuple(strategy_names)
        super().__init__(shape=(), dtype=np.str_)

    def sample(self, mask=None, probability=None) -> str:
        if len(self.strategy_names) == 0:
            raise ValueError("Cannot sample from an empty strategy action space")

        index = self.np_random.integers(len(self.strategy_names))
        return self.strategy_names[int(index)]

    def contains(self, x: Any) -> bool:
        return isinstance(x, str) and x in self.strategy_names

    def __contains__(self, x: Any) -> bool:
        return self.contains(x)

    def __iter__(self):
        return iter(self.strategy_names)

    def __len__(self) -> int:
        return len(self.strategy_names)

    def __repr__(self) -> str:
        return f"StrategyActionSpace({list(self.strategy_names)!r})"


class CodeHackWrapper(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        strategies: List[Callable],
        panics: List[Callable],
        max_strategy_steps: int = 1000,
        gamma: float = 0.99,
        primitives: Optional[List[str]] = None,
        no_strategy_progress_timeout: int = 150,
    ) -> None:
        super().__init__(env)
        if max_strategy_steps is None:
            max_strategy_steps = env.unwrapped._max_episode_steps
        primitives = primitives or []

        self.bot = Bot(
            env,
            max_strategy_steps=max_strategy_steps,
            gamma=gamma,
            no_strategy_progress_timeout=no_strategy_progress_timeout,
        )

        if len(primitives) > 0:
            self.bot.register_primitives(primitives)

        for panic_func in panics:
            self.bot.panic(panic_func)

        for strategy_func in strategies:
            self.bot.strategy(strategy_func)

        self.action_space = StrategyActionSpace(self.bot.strategies)
        self.observation_space = gym.spaces.Dict(
            {"env_steps": gym.spaces.Box(low=0, high=255, shape=(1,)), **self.env.observation_space}
        )

    def reset(self, **kwargs) -> Tuple[Dict[str, ndarray], Dict[str, Any]]:
        obs, info = self.bot.reset(**kwargs)
        obs["env_steps"] = np.array([info["episode_extra_stats"]["env_steps"]])

        return obs, info

    def step(self, action: str) -> Tuple[Dict[str, ndarray], float, bool, bool, Dict[str, Any]]:
        if action not in self.action_space:
            raise ValueError(f"Unknown strategy action: {action!r}")

        obs, reward, terminated, truncated, info = self.bot.strategy_step(action)
        obs["env_steps"] = np.array([info["episode_extra_stats"]["env_steps"]])

        return obs, reward, terminated, truncated, info
