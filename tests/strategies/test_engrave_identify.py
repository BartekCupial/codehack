import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotFinished, BotPanic
from codehack.bot.strategies import (
    descend_stairs,
    engrave_elbereth,
    engrave_identify,
    explore_corridor,
    explore_room,
    fight_multiple_monsters,
    fight_ranged,
    goto_corridor,
    goto_room,
    goto_unexplored_room,
    open_doors,
    pickup_wand,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestEngraveIdentify:
    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-EngraveIdentify-v0",
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

        pickup_wand(bot)
        goto_corridor(bot)
        goto_room(bot)
        engrave_identify(bot)
