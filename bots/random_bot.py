import numpy as np

from .AsyncBot import AsyncBot


class RandomAsyncBot(AsyncBot):
    def act(self, state):
        mouse = np.random.random(2) - 0.5
        keyboard = (np.random.random(1) < 0.1).astype(np.float32)
        return np.concatenate((mouse, keyboard))


class RandomSyncBot:
    def __call__(self, state):
        action = np.random.random(3)
        return action
