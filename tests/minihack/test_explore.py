import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotPanic
from codehack.bot.strategies import descend_stairs, explore_room
from codehack.envs.minihack.play_minihack import parse_minihack_args


@pytest.mark.usefixtures("register_components")
class TestMazewalkMapped(object):
    @pytest.mark.parametrize(
        "env",
        [
            "MiniHack-ExploreMaze-Easy-v0",
            "MiniHack-ExploreMaze-Easy-Mapped-v0",
            "MiniHack-ExploreMaze-Hard-v0",
            "MiniHack-ExploreMaze-Hard-Mapped-v0",
            "MiniHack-Labyrinth-Small-v0",
        ],
    )
    def test_solve_explore(self, env):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
            ]
        )

        def solve(bot: "Bot"):
            while True:
                try:
                    if descend_stairs(bot):
                        pass
                    else:
                        explore_room(bot)
                except BotPanic:
                    pass

        cfg.strategies = [solve]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"
