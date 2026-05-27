from codehack.envs.minihack.resources import des_file
from minihack.envs import register
from minihack.envs.corridor import MiniHackCorridor


class MiniHackPremappedCorridor2(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file=des_file("premapped_corridor2.des"), **kwargs)


class MiniHackPremappedCorridor3(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file=des_file("premapped_corridor3.des"), **kwargs)


class MiniHackPremappedCorridor5(MiniHackCorridor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file=des_file("premapped_corridor5.des"), **kwargs)


register(
    id="CustomMiniHack-Premapped-Corridor-R2-v0",
    entry_point="codehack.envs.minihack.envs.premapped_corridor:MiniHackPremappedCorridor2",
)

register(
    id="CustomMiniHack-Premapped-Corridor-R3-v0",
    entry_point="codehack.envs.minihack.envs.premapped_corridor:MiniHackPremappedCorridor3",
)

register(
    id="CustomMiniHack-Premapped-Corridor-R5-v0",
    entry_point="codehack.envs.minihack.envs.premapped_corridor:MiniHackPremappedCorridor5",
)
