import pytest
from nle_utils.task_rewards import OracleScore

from codehack.bot.strategies import goto_room
from codehack.envs.minihack.play_minihack import parse_minihack_args
from codehack.utils import utils
from codehack.utils.tests import create_bot

# @pytest.mark.usefixtures("register_components")
# class TestOracle(object):
#     @pytest.mark.parametrize("env", ["CustomMiniHack-Oracle-v0"])
#     @pytest.mark.parametrize("seed", [0])
#     def test_corridor_detection(self, env, seed):
#         """
#         check if corridors are detected correctly:
#         """
#         cfg = parse_minihack_args(
#             argv=[
#                 f"--env={env}",
#                 f"--seed={seed}",
#                 "--codehack=False",
#                 "--no-render",
#             ]
#         )
#         task = OracleScore()
#         bot = create_bot(cfg)
#         bot.reset(seed=seed)

#         inner_env = bot.env.unwrapped
#         assert 0 == task.reward(inner_env, None, inner_env.last_observation, None)
#         goto_room(bot)
#         # oracle detection
#         assert 1 == task.reward(inner_env, None, inner_env.last_observation, None)
