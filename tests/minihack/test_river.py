import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotPanic
from codehack.bot.strategies import (
    align_boulder_for_bridge,
    descend_stairs,
    explore_room,
    goto_boulder_closest_to_river,
    push_boulder_into_river,
    push_boulder_south,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args


def solve(bot: "Bot"):
    while True:
        try:
            explore_room(bot)
            goto_boulder_closest_to_river(bot)
            align_boulder_for_bridge(bot)
            push_boulder_into_river(bot)
            descend_stairs(bot)
        except BotPanic:
            push_boulder_south(bot)
            push_boulder_south(bot)


@pytest.mark.usefixtures("register_components")
class TestRiver(object):
    @pytest.mark.parametrize(
        "env",
        [
            "MiniHack-River-v0",
        ],
    )
    @pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
    def test_river(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )
        cfg.strategies = [solve]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"
