import numpy

from .Bot import Bot


class RandomBot(Bot):
    def act(self, state):
        return numpy.random.random(2) - 0.5
