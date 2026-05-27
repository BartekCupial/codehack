import pytest

from codehack.bot.strategies import explore_corridor_systematically, goto_corridor, goto_room, open_doors
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils import utils
from codehack.utils.strategies import corridor_detection
from codehack.utils.tests import create_bot


@pytest.mark.usefixtures("register_components")
class TestFeatures(object):
    @pytest.mark.parametrize("env", ["CustomMiniHack-Premapped-Corridor-R5-v0"])
    @pytest.mark.parametrize("seed", [0])
    def test_corridor_detection(self, env, seed):
        """
        check if corridors are detected correctly:
        """
        cfg = parse_minihack_args(
            argv=[
                f"--env={env}",
                f"--seed={seed}",
                "--codehack=False",
                "--no-render",
            ]
        )
        bot = create_bot(cfg)
        bot.reset(seed=seed)

        room_position = bot.entity.position

        # - when we are in doors
        goto_corridor(bot)
        labeled_corridors, num_corridors = corridor_detection(bot)
        door_position = bot.entity.position
        assert labeled_corridors[door_position] != 0
        assert labeled_corridors[room_position] == 0

        # - when we are in corridor
        explore_corridor_systematically(bot)
        labeled_corridors, num_corridors = corridor_detection(bot)
        corridor_position = bot.entity.position
        assert labeled_corridors[door_position] != 0
        assert labeled_corridors[corridor_position] != 0
        assert labeled_corridors[room_position] == 0

        # - when we are in room
        open_doors(bot)
        goto_room(bot)
        labeled_corridors, num_corridors = corridor_detection(bot)
        assert labeled_corridors[door_position] != 0
        assert labeled_corridors[corridor_position] != 0
        assert labeled_corridors[room_position] == 0
