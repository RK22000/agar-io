import numpy


class RandomBot:
    def __call__(self, x):
        return numpy.random.random(2) - 0.5