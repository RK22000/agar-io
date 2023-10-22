import numpy as np

from .Bot import Bot


class RandomBot(Bot):
    def act(self, state):
        mouse = np.random.random(2) - 0.5
        keyboard = (np.random.random(1) < 0.1).astype(np.float32)
        return np.concatenate((mouse, keyboard))
