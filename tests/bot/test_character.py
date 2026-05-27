import pytest

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
    def test_parse_character(self, env):
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                "--character=@",
                "--no-render",
                "--codehack=False",
            ]
        )
        bot = create_bot(cfg)
        for i in range(1000):
            bot.reset(seed=i)
            str(bot.character)
