import pytest

from codehack.envs.minihack.play_minihack import register_minihack_components


@pytest.fixture(scope="session", autouse=True)
def register_components():
    register_minihack_components()
