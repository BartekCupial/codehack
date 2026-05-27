import gymnasium as gym
from gymnasium.utils import seeding


class MiniHackSeedCompat(gym.Wrapper):
    def reset(self, seed=None, **kwargs):
        if seed is not None:
            self._seed(seed)

        return self.env.reset(seed=seed, **kwargs)

    def _seed(self, seed):
        if self._needs_modern_minigrid_seed():
            self._seed_modern_minigrid(seed)
            self._seed_nethack(seed)
        else:
            self.env.unwrapped.seed(seed, seed, reseed=False)

    def _needs_modern_minigrid_seed(self):
        base_env = self.env.unwrapped
        if not hasattr(base_env, "minigrid_env"):
            return False

        return not hasattr(base_env.minigrid_env.unwrapped, "seed")

    def _seed_modern_minigrid(self, seed):
        rng, _ = seeding.np_random(seed)
        self.env.unwrapped.minigrid_env.unwrapped.np_random = rng

    def _seed_nethack(self, seed):
        from minihack import MiniHackNavigation

        MiniHackNavigation.seed(self.env.unwrapped, seed, seed, reseed=False)
