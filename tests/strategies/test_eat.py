import pytest

from codehack.bot.strategies import (
    eat_corpse_floor,
    eat_corpse_inventory,
    eat_food_inventory,
    goto_corpse,
    pickup_corpse,
    pickup_food,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestEat:
    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-Corpse-v0",
        ],
    )
    @pytest.mark.parametrize("seed", list(range(2)))
    def test_eat_corpse_floor(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--no-render",
                "--codehack=False",
            ]
        )
        bot = create_bot(cfg)
        bot.reset(seed=seed)

        pickup_food(bot)
        goto_corpse(bot)
        assert eat_corpse_floor(bot)

    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-Corpse-v0",
        ],
    )
    @pytest.mark.parametrize("seed", list(range(2)))
    def test_eat_corpse_inventory(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--no-render",
                "--codehack=False",
            ]
        )
        bot = create_bot(cfg)
        bot.reset(seed=seed)

        pickup_food(bot)
        pickup_food(bot)
        pickup_corpse(bot)
        assert eat_corpse_inventory(bot)

    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-Corpse-v0",
        ],
    )
    @pytest.mark.parametrize("seed", list(range(3)))
    def test_eat_food_inventory(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--no-render",
                "--codehack=False",
            ]
        )
        bot = create_bot(cfg)
        bot.reset(seed=seed)

        pickup_corpse(bot)
        pickup_food(bot)
        assert eat_food_inventory(bot)
