from typing import Callable

import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotPanic
from codehack.bot.strategies import (
    descend_stairs,
    eat_food_inventory,
    explore_room,
    fight_melee,
    goto_unexplored_corridor,
    goto_unexplored_room,
    open_doors_kick,
    pickup_amulet,
    pickup_armor,
    pickup_food,
    pickup_scroll,
    pickup_wand,
    puton_amulet,
    quaff_sink,
    read_scroll,
    wear_cloak,
    zap_wand,
)
from codehack.bot.strategies.goto import goto_closest
from codehack.envs.minihack.play_minihack import parse_minihack_args


def general_mini(bot: "Bot", action: Callable):
    while True:
        fight_melee(bot)
        explore_room(bot)
        action(bot)


def make_pickup_and_act(pickup: Callable, act: Callable) -> Callable:
    def pickup_and_act(bot: "Bot"):
        pickup(bot)
        act(bot)

    pickup_and_act.__name__ = f"{pickup.__name__}_{act.__name__}"
    return pickup_and_act


def make_general_mini(action: Callable) -> Callable:
    def solve(bot: "Bot"):
        general_mini(bot, action=action)

    solve.__name__ = f"general_mini_{action.__name__}"
    return solve


def pray_altar_immediately(bot: "Bot"):
    features = bot.terrain_features[bot.blstats.dungeon_number, bot.blstats.level_number].get("features", {})
    if goto_closest(bot, features.get("altar", [])):
        return bot.pray()

    return False


@pytest.mark.usefixtures("register_components")
class TestMazewalkMapped(object):
    @pytest.mark.parametrize("env", ["MiniHack-LockedDoor-Fixed-v0"])
    @pytest.mark.parametrize("seed", list(range(5)))
    def test_mini_locked(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )

        def solve(bot: "Bot"):
            while True:
                try:
                    open_doors_kick(bot)
                    explore_room(bot)
                    descend_stairs(bot)
                except BotPanic:
                    pass

        cfg.strategies = [solve]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"

    @pytest.mark.parametrize("env", ["MiniHack-LockedDoor-v0"])
    @pytest.mark.parametrize("seed", list(range(5)))
    def test_mini_locked_dynamic(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )

        def solve(bot: "Bot"):
            while True:
                try:
                    open_doors_kick(bot)
                    explore_room(bot)
                    goto_unexplored_corridor(bot)
                    goto_unexplored_room(bot)
                    descend_stairs(bot)
                except BotPanic:
                    pass

        cfg.strategies = [solve]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"

    @pytest.mark.parametrize(
        "env, action",
        [
            ("MiniHack-Eat-v0", make_pickup_and_act(pickup_food, eat_food_inventory)),
            ("MiniHack-Read-v0", make_pickup_and_act(pickup_scroll, read_scroll)),
            ("MiniHack-Zap-v0", make_pickup_and_act(pickup_wand, zap_wand)),
            ("MiniHack-PutOn-v0", make_pickup_and_act(pickup_amulet, puton_amulet)),
            ("MiniHack-Wear-v0", make_pickup_and_act(pickup_armor, wear_cloak)),
            # doesn't work because we wield best weapon and here dagger is worse
            # ("MiniHack-Wield-v0", make_pickup_and_act(pickup_weapon, wield_melee_weapon)),
            ("MiniHack-Eat-Distr-v0", make_pickup_and_act(pickup_food, eat_food_inventory)),
            ("MiniHack-Read-Distr-v0", make_pickup_and_act(pickup_scroll, read_scroll)),
            ("MiniHack-Zap-Distr-v0", make_pickup_and_act(pickup_wand, zap_wand)),
            ("MiniHack-PutOn-Distr-v0", make_pickup_and_act(pickup_amulet, puton_amulet)),
            ("MiniHack-Wear-Distr-v0", make_pickup_and_act(pickup_armor, wear_cloak)),
            # doesn't work because we wield best weapon and here dagger is worse
            # ("MiniHack-Wield-Distr-v0", make_pickup_and_act(pickup_weapon, wield_melee_weapon)),
        ],
    )
    @pytest.mark.parametrize("seed", list(range(5)))
    def test_mini(self, env, action, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )
        cfg.strategies = [make_general_mini(action)]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"

    @pytest.mark.parametrize(
        "env, action",
        [
            ("MiniHack-Pray-v0", pray_altar_immediately),
            ("MiniHack-Sink-v0", quaff_sink),
            ("MiniHack-Pray-Distr-v0", pray_altar_immediately),
            ("MiniHack-Sink-Distr-v0", quaff_sink),
        ],
    )
    @pytest.mark.parametrize("seed", list(range(5)))
    def test_mini_special(self, env, action, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )
        cfg.strategies = [make_general_mini(action)]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"
