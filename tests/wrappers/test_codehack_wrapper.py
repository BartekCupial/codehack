import numpy as np
import pytest

import codehack.wrappers.codehack_wrapper as wrapper_module


class DummyBot:
    def __init__(self, *args, **kwargs):
        self.strategies = {}
        self.strategy_actions = []

    def strategy(self, func):
        self.strategies[func.__name__] = func

    def panic(self, func):
        pass

    def strategy_step(self, action):
        self.strategies[action]
        self.strategy_actions.append(action)

        obs = {"dummy": np.array([0], dtype=np.uint8)}
        info = {"episode_extra_stats": {"env_steps": 0}}

        return obs, 0.0, False, False, info


class DummyEnv:
    @property
    def unwrapped(self):
        return self

    @property
    def observation_space(self):
        return {}


def first_strategy(bot):
    pass


def second_strategy(bot):
    pass


@pytest.fixture
def wrapper(monkeypatch):
    monkeypatch.setattr(wrapper_module, "Bot", DummyBot)

    return wrapper_module.CodeHackWrapper(DummyEnv(), [first_strategy, second_strategy], [])


def test_action_space_exposes_strategy_names(wrapper):
    assert list(wrapper.action_space) == ["first_strategy", "second_strategy"]
    assert "first_strategy" in wrapper.action_space
    assert 0 not in wrapper.action_space
    assert wrapper.action_space.sample() in wrapper.action_space


def test_step_uses_strategy_names(wrapper):
    wrapper.step("second_strategy")

    assert wrapper.bot.strategy_actions == ["second_strategy"]


def test_step_rejects_integer_actions(wrapper):
    with pytest.raises(ValueError, match="Unknown strategy action: 0"):
        wrapper.step(0)
