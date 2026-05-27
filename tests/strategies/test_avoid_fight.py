import pytest

from codehack.bot.exceptions import BotFinished
from codehack.bot.strategies import approach_monster, descend_stairs, explore_corridor, goto_corridor, goto_room
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils import utils
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestAvoidFight(object):
    @pytest.mark.parametrize("env", ["CustomMiniHack-AvoidFight-Still-v0"])
    @pytest.mark.parametrize("seed", [1])
    def test_still(self, env, seed):
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

        try:
            goto_corridor(bot)
            explore_corridor(bot)
            goto_room(bot)
            approach_monster(bot)
            descend_stairs(bot)
        except BotFinished:
            pass

    @pytest.mark.parametrize("env", ["CustomMiniHack-AvoidFight-Moving-v0"])
    @pytest.mark.parametrize("seed", [1])
    def test_moving(self, env, seed):
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

        try:
            goto_corridor(bot)
            explore_corridor(bot)
            goto_room(bot)
            approach_monster(bot)
            descend_stairs(bot)
        except BotFinished:
            pass
