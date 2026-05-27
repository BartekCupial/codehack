import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotFinished, BotPanic
from codehack.bot.strategies import (
    descend_stairs,
    examine_items,
    explore_corridor,
    explore_room,
    fight_multiple_monsters,
    fight_ranged,
    goto_corridor,
    goto_room,
    goto_unexplored_room,
    open_doors,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestFightRanged:
    @pytest.mark.parametrize(
        "env",
        [
            "CustomMiniHack-FightRanged-v0",
        ],
    )
    @pytest.mark.parametrize("seed", list(range(3)))
    def test_fight_ranged(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--no-render",
                "--autopickup=True",
                "--codehack=False",
            ]
        )

        bot = create_bot(cfg)
        bot.reset(seed=seed)

        examine_items(bot)
        goto_corridor(bot)
        while fight_ranged(bot):
            pass
        with pytest.raises(BotFinished):
            descend_stairs(bot)
