import pytest

from codehack.bot.strategies import (
    goto_corridor,
    goto_room,
    pickup_ring,
    pickup_scroll,
    puton_ring,
    read_scroll,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestEngraveIdentify:
    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-ReadScroll-v0",
        ],
    )
    @pytest.mark.parametrize("seed", list(range(3)))
    def test_engrave(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--no-render",
                "--autopickup=True",
                "--codehack=False",
                "--max_strategy_steps=1000",
            ]
        )

        bot = create_bot(cfg)
        bot.reset(seed=seed)

        pickup_ring(bot)
        pickup_scroll(bot)
        goto_corridor(bot)
        goto_room(bot)
        puton_ring(bot)
        puton_ring(bot)
        while read_scroll(bot):
            pass
