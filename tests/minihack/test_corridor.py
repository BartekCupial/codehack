import pytest
from nle_utils.play import play

from codehack.bot.bot import Bot
from codehack.bot.exceptions import BotPanic
from codehack.bot.strategies import (
    descend_stairs,
    explore_corridor_systematically,
    explore_room,
    goto_corridor,
    goto_unexplored_room,
    open_doors_kick,
    search_corridor_for_hidden_doors,
    search_room_for_hidden_doors,
)
from codehack.envs.minihack.play_minihack import parse_minihack_args


@pytest.mark.usefixtures("register_components")
class TestMazewalkMapped(object):
    @pytest.mark.parametrize("env", ["MiniHack-Corridor-R2-v0", "MiniHack-Corridor-R3-v0", "MiniHack-Corridor-R5-v0"])
    @pytest.mark.parametrize("seed", list(range(10)))
    def test_corridor_open_doors(self, env, seed):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--no-render",
                f"--seed={seed}",
            ]
        )

        def general_solve(bot: "Bot"):
            room_searches = 0
            corridor_searches = 0

            def attempt(strategy):
                try:
                    return bool(strategy(bot))
                except BotPanic:
                    return False

            while True:
                for strategy in [
                    descend_stairs,
                    open_doors_kick,
                    explore_room,
                    explore_corridor_systematically,
                    goto_unexplored_room,
                    goto_corridor,
                ]:
                    attempt(strategy)

                if bot.blstats.hunger_state < 2 and corridor_searches == 0:
                    corridor_searches += 1
                    attempt(search_corridor_for_hidden_doors)

                if bot.blstats.hunger_state < 2 and room_searches == 0:
                    room_searches += 1
                    attempt(search_room_for_hidden_doors)

        cfg.strategies = [general_solve]
        status = play(cfg, get_action=lambda env, *_: list(env.action_space)[-1])
        assert status["end_status"].name == "TASK_SUCCESSFUL"
